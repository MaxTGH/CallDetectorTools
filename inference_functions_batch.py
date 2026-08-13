"""

Slower than the original version but explores batching as opposed to single image processing

Adapted from older version on August 15th 2025

@author: Michaela Alksne and Shane Andres

Contains helper functions for performing inference

"""

import yaml
import os
import torchvision.ops as ops
from PIL import Image
from spectrogram_functions import *
import time

saveSpect = False # do you want to save each spectrogram

def predict_and_save_spectrograms(wav_file_path, model, model_name, device):
    '''
    For one wav file,
    1) Performs inference on each chunk
    2) Saves the spectrogram for any chunk containing detections
    3) Returns all detections in a list
    Inputs:
    - wav_file_path: location of wav file to run inference on
    - model: the model to use
    - model_name: the name of the model (logged in the model output)
    - device: the torch device to store data on
    Outputs:
    - output: a list of dicts, where each dict stores information about one detection in the model output format
    '''

    # loading spectrogram settings
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    thresholds = config['inference']['thresholds']
    nms_threshold = config['inference']['nms_threshold']
    spectrogram_folder = config['inference']['spectrogram_folder']
    categories = config['categories']
    categories_rev = {v: k for k, v in categories.items()}

    # generating spectrograms
    wav_file_name = os.path.splitext(os.path.basename(wav_file_path))[0]
    wav_file_name = os.path.splitext(wav_file_path)[0]  # removes .x for xwav files

    chunks, chunk_start_times, chunk_end_times, sr = chunk_audio(
        wav_file_path, device
    )

    # -----------------------------
    # Preprocessing timing
    # -----------------------------
    t1 = time.perf_counter()
    spectrograms = chunk_to_spectrogram(chunks, sr, device)
    print(f"Preprocessing: {time.perf_counter() - t1:.2f}s")

    t0 = chunk_start_times[0]

    output = []

    batch_size = 16

    for start in range(0, len(spectrograms), batch_size):

        batch_specs = spectrograms[start:start + batch_size]
        batch_times = chunk_start_times[start:start + batch_size]

        print("Creating batch...")

        batch = (
            torch.stack(batch_specs)
            .unsqueeze(1)
            .float()
            .div(255)
            .to(device)
        )

        print(batch.shape)
        print(
            f"Processing batch starting at {start}. "
            f"Remaining images: {len(spectrograms) - start}"
        )

        print("Calling model...")

        # -----------------------------
        # Model timing
        # -----------------------------
        t1 = time.perf_counter()

        with torch.no_grad():
            predictions = model(batch)

        model_time = time.perf_counter() - t1

        print(
            f"Model: {model_time:.6f}s "
            f"({model_time / len(batch_specs):.6f}s/image)"
        )

        print("Model returned")

        # -----------------------------
        # Postprocessing timing
        # -----------------------------
        t1 = time.perf_counter()

        for spectrogram, chunk_start_time, prediction in zip(
            batch_specs,
            batch_times,
            predictions,
        ):

            boxes = prediction["boxes"]
            scores = prediction["scores"]
            labels = prediction["labels"]

            # apply non-maximum suppression (NMS)
            keep_indices = ops.nms(boxes, scores, nms_threshold)
            boxes = boxes[keep_indices]
            scores = scores[keep_indices]
            labels = labels[keep_indices]

            # check if there are valid predictions (boxes)
            if len(boxes) == 0:
                continue

            saved = False

            # save detections to output
            for box, score, label in zip(boxes, scores, labels):

                category = categories_rev.get(label.item(), "Unknown")

                if score.item() < thresholds.get(category, 0):
                    continue

                elif not saved:
                    spectrogram_file = os.path.basename(
                        name_spectrogram_file(
                            wav_file_name,
                            chunk_start_time
                        )
                    )

                    spectrogram_path = os.path.join(
                        spectrogram_folder,
                        spectrogram_file
                    )

                    spectrogram_img = Image.fromarray(
                        spectrogram.numpy()
                    )

                    if saveSpect:
                        spectrogram_img.save(spectrogram_path)

                    saved = True

                # get box time offsets
                x1, x2 = box[0].item(), box[2].item()
                y1, y2 = box[1].item(), box[3].item()

                start_offset_sec = pixel_to_time(x1)
                end_offset_sec = pixel_to_time(x2)

                # absolute seconds since WAV start (t0)
                chunk_start_sec = (
                    chunk_start_time - t0
                ).total_seconds()

                start_time_sec = (
                    chunk_start_sec + start_offset_sec
                )

                end_time_sec = (
                    chunk_start_sec + end_offset_sec
                )

                start_time = (
                    chunk_start_time
                    + timedelta(seconds=start_offset_sec)
                )

                end_time = (
                    chunk_start_time
                    + timedelta(seconds=end_offset_sec)
                )

                output.append({
                    'wav_file_path': wav_file_path,
                    'model_no': model_name,
                    'image_file_path': spectrogram_path,
                    'label': category,
                    'score': round(score.item(), 2),
                    'start_time_sec': start_time_sec,
                    'end_time_sec': end_time_sec,
                    'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'min_frequency': pixel_to_freq(y2),
                    'max_frequency': pixel_to_freq(y1),
                    'box_x1': x1,
                    'box_x2': x2,
                    'box_y1': y1,
                    'box_y2': y2
                })

        post_time = time.perf_counter() - t1

        print(
            f"Postprocessing: {post_time:.6f}s "
            f"({post_time / len(batch_specs):.6f}s/image)"
        )

    return output