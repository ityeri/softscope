import pyaudio

p = pyaudio.PyAudio()

all_devices = list()
stereo_devices = list()
other_devices = list()

for i in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(i)
    all_devices.append(device_info)

    if device_info['maxInputChannels'] == 2:
        stereo_devices.append(device_info)
    elif 0 < device_info['maxInputChannels']:
        other_devices.append(device_info)


max_number_length = max(map(lambda x: len(str(x)), range(len(all_devices))))
max_name_length = max(map(lambda x: len(x['name']), all_devices))
max_sample_rate_length = max(map(lambda x: len(str(x['defaultSampleRate'])), all_devices))
max_channels_length = max(map(lambda x: len(str(x['maxInputChannels'])), all_devices))


print('Stereo Devices:')
for i, device_info in enumerate(stereo_devices):
    print(
        f'{str(i).rjust(max_number_length)} - '
        f'Name: {device_info['name'].ljust(max_name_length)} | '
        f'Default sample rate: {str(device_info['defaultSampleRate']).ljust(max_sample_rate_length)}'
        f'Max input channels: {str(device_info['maxInputChannels']).ljust(max_channels_length)}'
    )

if not stereo_devices:
    print('...No device')

print()

print('Other Devices:')
for i, device_info in enumerate(other_devices):
    print(
        f'{str(i).rjust(max_number_length)} - '
        f'Name: {device_info['name'].ljust(max_name_length)} | '
        f'Default sample rate: {str(device_info['defaultSampleRate']).ljust(max_sample_rate_length)} | '
        f'Max input channels: {str(device_info['maxInputChannels']).ljust(max_channels_length)}'
    )

if not other_devices:
    print('No device')
