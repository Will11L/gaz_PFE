import nidaqmx
import numpy as np
import matplotlib.pyplot as plt
from nidaqmx.constants import AcquisitionType
import time

# Paramètres
sample_rate = 20000  # Taux d'échantillonnage en Hz (par exemple 10 kHz)
duration = 0.01  # Durée d'acquisition en secondes
num_samples = int(sample_rate * duration)  # Nombre d'échantillons à lire

# Initialisation du graphique
plt.ion()  # Mode interactif pour mise à jour du graphique en temps réel
fig, ax = plt.subplots()
xdata = np.linspace(0, duration, num_samples)
ydata = np.zeros(num_samples)
(line,) = ax.plot(xdata, ydata)

ax.set_ylim(-2.5, 2.5)  # Limites de tension (amplitude max de 2V pour votre signal sinusoïdal)
ax.set_xlim(0, duration)
ax.set_xlabel('Temps [s]')
ax.set_ylabel('Tension [V]')
plt.title('Signal sinusoïdal 1 kHz')

# Lire les données en temps réel
with nidaqmx.Task() as task:
    # Ajouter le canal analogique ai0 pour lire le signal
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    
    # Configurer la tâche pour lecture continue avec un taux d'échantillonnage défini
    task.timing.cfg_samp_clk_timing(sample_rate, sample_mode=AcquisitionType.FINITE, samps_per_chan=num_samples)
    
    print("Lecture des données... Appuyez sur Ctrl+C pour arrêter.")

    try:
        while True:
            # Lire les échantillons depuis la carte
            data = task.read(number_of_samples_per_channel=num_samples)

            # Mise à jour des données sur le graphique
            line.set_ydata(data)
            fig.canvas.draw()
            fig.canvas.flush_events()
            
            time.sleep(0.1)  # Pause pour ne pas surcharger le processeur

    except KeyboardInterrupt:
        print("Lecture interrompue.")
