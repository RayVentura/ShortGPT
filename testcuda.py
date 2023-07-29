import tensorflow as tf

# Check TensorFlow version
print("TensorFlow version:", tf.__version__)

# Check if GPU is available
print("GPU available:", tf.test.is_gpu_available())

# Check CUDA version
print("CUDA version:", tf.test.gpu_device_name())

# Check cuDNN version
print("cuDNN version:", tf.test.is_built_with_cuda())

# Check GPU device name
physical_devices = tf.config.list_physical_devices('GPU')
if len(physical_devices) > 0:
    print("GPU device name:", physical_devices[0])
else:
    print("No GPU device found.")