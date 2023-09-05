from typing import Iterator, Tuple, Any

import glob
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow_hub as hub
import mediapy as media


class ImperialWristDataset(tfds.core.GeneratorBasedBuilder):
    """DatasetBuilder for example dataset."""

    VERSION = tfds.core.Version('1.0.0')
    RELEASE_NOTES = {
      '1.0.0': 'Initial release.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-large/5")

    def _info(self) -> tfds.core.DatasetInfo:
        """Dataset metadata (homepage, citation,...)."""
        return self.dataset_info_from_configs(
            features=tfds.features.FeaturesDict({
                'steps': tfds.features.Dataset({
                    'observation': tfds.features.FeaturesDict({
                        'image': tfds.features.Image(
                            shape=(64, 64, 3),
                            dtype=np.uint8,
                            encoding_format='png',
                            doc='Main camera RGB observation (same as wrist in our case).',
                        ),

                         'wrist_image': tfds.features.Image(
                            shape=(64, 64, 3),
                            dtype=np.uint8,
                            encoding_format='png',
                            doc='Wrist camera RGB observation.',
                         ),
                         'state': tfds.features.Tensor(
                            shape=(1,),
                            dtype=np.float32,
                            doc='Gripper state (opened or closed)',
                        ),

                    }),
                    'action': tfds.features.Tensor(
                        shape=(8,),
                        dtype=np.float32,
                        doc='Robot action, consists of 3x delta position in EEF frame, 3x delta ZYX euler angles, 1x gripper open/close, 1x terminate episode.',
                    ),
                    'discount': tfds.features.Scalar(
                        dtype=np.float32,
                        doc='Discount if provided, default to 1.'
                    ),
                    'reward': tfds.features.Scalar(
                        dtype=np.float32,
                        doc='Reward if provided, 1 on final step for demos.'
                    ),
                    'is_first': tfds.features.Scalar(
                        dtype=np.bool_,
                        doc='True on first step of the episode.'
                    ),
                    'is_last': tfds.features.Scalar(
                        dtype=np.bool_,
                        doc='True on last step of the episode.'
                    ),
                    'is_terminal': tfds.features.Scalar(
                        dtype=np.bool_,
                        doc='True on last step of the episode if it is a terminal step, True for demos.'
                    ),
                    'language_instruction': tfds.features.Text(
                        doc='Language Instruction.'
                    ),
                    'language_embedding': tfds.features.Tensor(
                        shape=(512,),
                        dtype=np.float32,
                        doc='Kona language embedding. '
                            'See https://tfhub.dev/google/universal-sentence-encoder-large/5'
                    ),
                }),
                'episode_metadata': tfds.features.FeaturesDict({
                    'file_path': tfds.features.Text(
                        doc='Path to the original data file.'
                    ),
                }),
            }))

    def _split_generators(self, dl_manager: tfds.download.DownloadManager):
        """Define data splits."""
        return {
            'train': self._generate_examples(path='/home/norman/Downloads/bc'),
        }

    def _generate_examples(self, path) -> Iterator[Tuple[str, Any]]:
        """Generator of examples for each split."""

        def _parse_example(episode_path, id):
            print(episode_path, id)
            # load raw data --> this should change for your dataset
            obs = np.load(episode_path + f"/observations_{id}.npy", allow_pickle=True)     # this is a list of dicts in our case
            acts = np.load(episode_path + f"/actions_{id}.npy", allow_pickle=True) 
            # assemble episode --> here we're assuming demos so we set reward to 1 at the end
            episode = []
            language_instruction = episode_path.split("/")[-1][:-1].replace("_", " ")
            for i, step in enumerate(obs):
                # compute Kona language embedding
                language_embedding = self._embed([language_instruction])[0].numpy()

                episode.append({
                    'observation': {
                        'image': media.resize_image(obs[i], (64,64)),
                        'wrist_image': media.resize_image(obs[i],(64,64)),
                        'state': [acts[i,-2]],
                        
                    },
                    'action': acts[i],
                    'discount': 1.0,
                    'reward': float(i == (len(obs) - 1)),
                    'is_first': i == 0,
                    'is_last': i == (len(obs) - 1),
                    'is_terminal': i == (len(obs) - 1),
                    'language_instruction': language_instruction,
                    'language_embedding': language_embedding,
                })

            # create output data sample
            sample = {
                'steps': episode,
                'episode_metadata': {
                    'file_path': episode_path
                }
            }

            # if you want to skip an example for whatever reason, simply return None
            return episode_path + f"_id_{id}", sample

        # create list of all examples
        episode_folders = glob.glob(path + "/*2")

        # for smallish datasets, use single-thread parsing
        for sample in episode_folders:
            for i in range(10):
                yield _parse_example(sample, i)

        # for large datasets use beam to parallelize data parsing (this will have initialization overhead)
        # beam = tfds.core.lazy_imports.apache_beam
        # return (
        #         beam.Create(episode_paths)
        #         | beam.Map(_parse_example)
        # )

