Here is the output as of 6b74322.

```console
$ . activate.sh

$ python main.py
NOW RUN create_ome_zarr (is it parallel? False)
[create_ome_zarr] START
[create_ome_zarr] image_dir='/tmp/input_images'
[create_ome_zarr] root_dir='/tmp/somewhere/'
[create_ome_zarr] zarr_path='/tmp/somewhere/my_plate.zarr'
[create_ome_zarr] END
Task output:
{
  "new_images": [
    {
      "path": "my_plate.zarr/A/01/0",
      "plate": "my_plate.zarr",
      "well": "A_01"
    },
    {
      "path": "my_plate.zarr/A/02/0",
      "plate": "my_plate.zarr",
      "well": "A_02"
    }
  ],
  "buffer": {
    "image_raw_paths": {
      "my_plate.zarr/A/01/0": "/tmp/input_images/figure_A01.tif",
      "my_plate.zarr/A/02/0": "/tmp/input_images/figure_A02.tif"
    }
  },
  "new_filters": {
    "plate": "my_plate.zarr"
  }
}
AFTER RUNNING create_ome_zarr:
{
  "id": 123,
  "root_dir": "/tmp/somewhere/",
  "images": [
    {
      "path": "my_plate.zarr/A/01/0",
      "plate": "my_plate.zarr",
      "well": "A_01"
    },
    {
      "path": "my_plate.zarr/A/02/0",
      "plate": "my_plate.zarr",
      "well": "A_02"
    }
  ],
  "default_filters": {
    "plate": "my_plate.zarr"
  },
  "buffer": {
    "image_raw_paths": {
      "my_plate.zarr/A/01/0": "/tmp/input_images/figure_A01.tif",
      "my_plate.zarr/A/02/0": "/tmp/input_images/figure_A02.tif"
    }
  },
  "history": [
    "create_ome_zarr"
  ]
}

----------------------------------------------------------------------------------------

NOW RUN yokogawa_to_zarr (is it parallel? True)
Current filters:     {
  "plate": "my_plate.zarr"
}
Filtered image list: [
  {
    "path": "my_plate.zarr/A/01/0",
    "plate": "my_plate.zarr",
    "well": "A_01"
  },
  {
    "path": "my_plate.zarr/A/02/0",
    "plate": "my_plate.zarr",
    "well": "A_02"
  }
]
[yokogawa_to_zarr] START
[yokogawa_to_zarr] root_dir='/tmp/somewhere/'
[yokogawa_to_zarr] component='my_plate.zarr/A/01/0'
[yokogawa_to_zarr] source_data='/tmp/input_images/figure_A01.tif'
[yokogawa_to_zarr] END
[yokogawa_to_zarr] START
[yokogawa_to_zarr] root_dir='/tmp/somewhere/'
[yokogawa_to_zarr] component='my_plate.zarr/A/02/0'
[yokogawa_to_zarr] source_data='/tmp/input_images/figure_A02.tif'
[yokogawa_to_zarr] END
Merged task output:
{}
AFTER RUNNING yokogawa_to_zarr:
{
  "id": 123,
  "root_dir": "/tmp/somewhere/",
  "images": [
    {
      "path": "my_plate.zarr/A/01/0",
      "plate": "my_plate.zarr",
      "well": "A_01"
    },
    {
      "path": "my_plate.zarr/A/02/0",
      "plate": "my_plate.zarr",
      "well": "A_02"
    }
  ],
  "default_filters": {
    "plate": "my_plate.zarr"
  },
  "buffer": null,
  "history": [
    "create_ome_zarr",
    "yokogawa_to_zarr"
  ]
}

----------------------------------------------------------------------------------------

NOW RUN illumination_correction (is it parallel? True)
Current filters:     {
  "plate": "my_plate.zarr"
}
Filtered image list: [
  {
    "path": "my_plate.zarr/A/01/0",
    "plate": "my_plate.zarr",
    "well": "A_01"
  },
  {
    "path": "my_plate.zarr/A/02/0",
    "plate": "my_plate.zarr",
    "well": "A_02"
  }
]
[illumination_correction] START
[illumination_correction] root_dir='/tmp/somewhere/'
[illumination_correction] component='my_plate.zarr/A/01/0'
[illumination_correction] new_component='my_plate.zarr/A/01/0_corr'
[illumination_correction] out={'new_images': [{'path': 'my_plate.zarr/A/01/0_corr', 'illumination_correction': True, 'plate': 'my_plate.zarr', 'well': 'A_01'}], 'new_filters': {'illumination_correction': True}}
[illumination_correction] END
[illumination_correction] START
[illumination_correction] root_dir='/tmp/somewhere/'
[illumination_correction] component='my_plate.zarr/A/02/0'
[illumination_correction] new_component='my_plate.zarr/A/02/0_corr'
[illumination_correction] out={'new_images': [{'path': 'my_plate.zarr/A/02/0_corr', 'illumination_correction': True, 'plate': 'my_plate.zarr', 'well': 'A_02'}], 'new_filters': {'illumination_correction': True}}
[illumination_correction] END
Merged task output:
{
  "new_images": [
    {
      "path": "my_plate.zarr/A/01/0_corr",
      "illumination_correction": true,
      "plate": "my_plate.zarr",
      "well": "A_01"
    },
    {
      "path": "my_plate.zarr/A/02/0_corr",
      "illumination_correction": true,
      "plate": "my_plate.zarr",
      "well": "A_02"
    }
  ],
  "new_filters": {
    "illumination_correction": true
  }
}
AFTER RUNNING illumination_correction:
{
  "id": 123,
  "root_dir": "/tmp/somewhere/",
  "images": [
    {
      "path": "my_plate.zarr/A/01/0",
      "plate": "my_plate.zarr",
      "well": "A_01"
    },
    {
      "path": "my_plate.zarr/A/02/0",
      "plate": "my_plate.zarr",
      "well": "A_02"
    },
    {
      "path": "my_plate.zarr/A/01/0_corr",
      "illumination_correction": true,
      "plate": "my_plate.zarr",
      "well": "A_01"
    },
    {
      "path": "my_plate.zarr/A/02/0_corr",
      "illumination_correction": true,
      "plate": "my_plate.zarr",
      "well": "A_02"
    }
  ],
  "default_filters": {
    "plate": "my_plate.zarr",
    "illumination_correction": true
  },
  "buffer": null,
  "history": [
    "create_ome_zarr",
    "yokogawa_to_zarr",
    "illumination_correction"
  ]
}

----------------------------------------------------------------------------------------

NOW RUN cellpose_segmentation (is it parallel? True)
Current filters:     {
  "plate": "my_plate.zarr",
  "illumination_correction": true
}
Filtered image list: [
  {
    "path": "my_plate.zarr/A/01/0_corr",
    "illumination_correction": true,
    "plate": "my_plate.zarr",
    "well": "A_01"
  },
  {
    "path": "my_plate.zarr/A/02/0_corr",
    "illumination_correction": true,
    "plate": "my_plate.zarr",
    "well": "A_02"
  }
]
[cellpose_segmentation] START
[cellpose_segmentation] root_dir='/tmp/somewhere/'
[cellpose_segmentation] component='my_plate.zarr/A/01/0_corr'
[cellpose_segmentation] out={}
[cellpose_segmentation] END
[cellpose_segmentation] START
[cellpose_segmentation] root_dir='/tmp/somewhere/'
[cellpose_segmentation] component='my_plate.zarr/A/02/0_corr'
[cellpose_segmentation] out={}
[cellpose_segmentation] END
Merged task output:
{}
AFTER RUNNING cellpose_segmentation:
{
  "id": 123,
  "root_dir": "/tmp/somewhere/",
  "images": [
    {
      "path": "my_plate.zarr/A/01/0",
      "plate": "my_plate.zarr",
      "well": "A_01"
    },
    {
      "path": "my_plate.zarr/A/02/0",
      "plate": "my_plate.zarr",
      "well": "A_02"
    },
    {
      "path": "my_plate.zarr/A/01/0_corr",
      "illumination_correction": true,
      "plate": "my_plate.zarr",
      "well": "A_01"
    },
    {
      "path": "my_plate.zarr/A/02/0_corr",
      "illumination_correction": true,
      "plate": "my_plate.zarr",
      "well": "A_02"
    }
  ],
  "default_filters": {
    "plate": "my_plate.zarr",
    "illumination_correction": true
  },
  "buffer": null,
  "history": [
    "create_ome_zarr",
    "yokogawa_to_zarr",
    "illumination_correction",
    "cellpose_segmentation"
  ]
}

----------------------------------------------------------------------------------------
```
