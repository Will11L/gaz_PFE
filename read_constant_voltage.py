# fichier: read_single_voltage.py
import nidaqmx
import numpy as np
import matplotlib.pyplot as plt
from nidaqmx.constants import AcquisitionType
import time

# Paramètres de lecture
sample_rate = 20000  # Taux d'échantillonnage en Hz
duration = 0.005     # Durée d'acquisition pour les lectures (réduite à 5 ms)
num_samples = int(sample_rate * duration)

# Initialisation du graphique pour un seul signal
plt.ion()  # Mode interactif pour mise à jour du graphique en temps réel
fig, ax = plt.subplots()
xdata = np.linspace(0, duration, num_samples)
ydata = np.zeros(num_samples)
line, = ax.plot(xdata, ydata, label='Canal ai0')

# Configuration du graphique
ax.set_ylim(-6, 6)  # Limites de tension pour ai0
ax.set_ylabel('Tension ai0 [V]')
ax.set_xlabel('Temps [s]')
ax.legend(loc="upper right")
plt.title('Lecture du signal continu sur ai0')

# Configuration de la tâche de lecture
with nidaqmx.Task() as read_task:
    # Ajouter le canal de lecture ai0
    read_task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    read_task.timing.cfg_samp_clk_timing(sample_rate, sample_mode=AcquisitionType.FINITE)

    # Augmenter la taille du tampon d'entrée
    read_task.in_stream.input_buf_size = 10 * num_samples

    print("Lecture de la tension sur ai0... Appuyez sur Ctrl+C pour arrêter.")

    try:
        while True:
            # Lire les échantillons depuis le canal ai0 avec timeout
            data = read_task.read(number_of_samples_per_channel=num_samples, timeout=10.0)

            # Convertir les données en un tableau NumPy si nécessaire
            data_ai0 = np.array(data)

            # Mise à jour du graphique
            line.set_ydata(data_ai0)
            fig.canvas.draw()
            fig.canvas.flush_events()

            # Pause pour l'affichage
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Lecture interrompue.")
