import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

# Data for SMPTE Audio levels - reference Level
smpte_ndi = np.array([0.0, 0.063, 0.1, 0.63, 1.0, 10.0])
smpte_dbu = np.array([-float('inf'), -20, -16, 0, 4, 24])
smpte_dbvu = np.array([-float('inf'), -24, -20, -4, 0, 20])
smpte_dbfs = np.array([-float('inf'), -44, -40, -24, -20, 0])

# Replace -inf with a lower value for plotting purposes
smpte_dbu = np.where(smpte_dbu == -float('inf'), -60, smpte_dbu)
smpte_dbvu = np.where(smpte_dbvu == -float('inf'), -60, smpte_dbvu)
smpte_dbfs = np.where(smpte_dbfs == -float('inf'), -60, smpte_dbfs)

# Logarithmic handling to avoid log(0)
smpte_ndi_log = np.array([0.001 if x == 0 else x for x in smpte_ndi])

# Data for EBU Audio levels - reference Level
ebu_ndi = np.array([0.0, 0.063, 0.1, 0.63, 1.0, 5.01])
ebu_dbu = np.array([-float('inf'), -20, -16, 0, 4, 18])
ebu_dbvu = np.array([-float('inf'), -24, -20, -4, 0, 14])
ebu_dbfs = np.array([-float('inf'), -38, -34, -18, -14, 0])

# Replace -inf with a lower value for plotting purposes
ebu_dbu = np.where(ebu_dbu == -float('inf'), -60, ebu_dbu)
ebu_dbvu = np.where(ebu_dbvu == -float('inf'), -60, ebu_dbvu)
ebu_dbfs = np.where(ebu_dbfs == -float('inf'), -60, ebu_dbfs)

# Logarithmic handling to avoid log(0)
ebu_ndi_log = np.array([0.001 if x == 0 else x for x in ebu_ndi])

# Labeling the NDI values
ndi_labels_smpte = ['0.0', '0.063', '0.1', '0.63', '1.0', '10.0']
ndi_labels_ebu = ['0.0', '0.063', '0.1', '0.63', '1.0', '5.01']

def plot_audio_levels(log_scale, standard):
    fig, ax = plt.subplots(figsize=(12, 8))

    if standard == 'SMPTE':
        ndi = smpte_ndi_log if log_scale else smpte_ndi
        dbu = smpte_dbu
        dbvu = smpte_dbvu
        dbfs = smpte_dbfs
        labels = ndi_labels_smpte
        title = 'SMPTE Audio Levels - Reference Level'
    else:
        ndi = ebu_ndi_log if log_scale else ebu_ndi
        dbu = ebu_dbu
        dbvu = ebu_dbvu
        dbfs = ebu_dbfs
        labels = ndi_labels_ebu
        title = 'EBU Audio Levels - Reference Level'

    # dBu vs NDI
    ax.plot(ndi, dbu, marker='o', linestyle='-', color='b', label='dBu')
    # dBVU vs NDI
    ax.plot(ndi, dbvu, marker='s', linestyle='--', color='g', label='dBVU')
    # dBFS vs NDI
    ax.plot(ndi, dbfs, marker='^', linestyle='-.', color='r', label='dBFS')

    # Set xticks and labels
    ax.set_xticks(ndi)
    ax.set_xticklabels(labels)

    # Toggle logarithmic scale
    if log_scale:
        ax.set_xscale('log')
    else:
        ax.set_xscale('linear')

    # Adding labels for points
    for i, txt in enumerate(dbu):
        ax.annotate(f'{txt} dB', (ndi[i], dbu[i]), textcoords="offset points", xytext=(0,10), ha='center')
    for i, txt in enumerate(dbvu):
        ax.annotate(f'{txt} dB', (ndi[i], dbvu[i]), textcoords="offset points", xytext=(0,10), ha='center')
    for i, txt in enumerate(dbfs):
        ax.annotate(f'{txt} dB', (ndi[i], dbfs[i]), textcoords="offset points", xytext=(0,10), ha='center')

    # Titles and labels
    ax.set_title(title)
    ax.set_xlabel('NDI')
    ax.set_ylabel('Audio Level (dB)')
    ax.legend()
    ax.grid(True)

    # Show plot
    plt.tight_layout()
    plt.show()

def convert_audio_sample(standard, floating_point_value):
    if standard == 'SMPTE':
        multiplier = 3276.8
    elif standard == 'EBU':
        multiplier = 6540.52
    else:
        raise ValueError("Invalid standard. Please choose 'SMPTE' or 'EBU'.")
    
    return max(-32768, min(32767, int(multiplier * floating_point_value)))


while True:
    print("Select the audio standard to plot:")
    print("1. SMPTE")
    print("2. EBU")
    print("3. Exit")
    standard_choice = input("Enter your choice (1, 2, or 3): ")

    if standard_choice not in ['1', '2', '3']:
        print("Invalid choice. Please select 1, 2, or 3.")
        continue

    if standard_choice == '3':
        break

    standard = 'SMPTE' if standard_choice == '1' else 'EBU'

    while True:
        print(f"Select an option for {standard}:")
        print("1. Linear Scale Plot")
        print("2. Logarithmic Scale Plot")
        print("3. Convert Floating-point to Integer Audio Value")
        print("4. Back to Standard Selection")
        view_choice = input("Enter your choice (1, 2, 3, or 4): ")

        if view_choice not in ['1', '2', '3', '4']:
            print("Invalid choice. Please select 1, 2, 3, or 4.")
            continue

        if view_choice == '4':
            break

        if view_choice == '1':
            plot_audio_levels(False, standard)
        elif view_choice == '2':
            plot_audio_levels(True, standard)
        elif view_choice == '3':
            try:
                floating_point_value = float(input("Enter the floating-point audio value: "))
                int_value = convert_audio_sample(standard, floating_point_value)
                print(f"The integer audio value is: {int_value}")
            except ValueError:
                print("Invalid input. Please enter a valid floating-point number.")
