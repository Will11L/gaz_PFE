import nidaqmx
import numpy as np
import time

# Paramètres pour générer un signal sinusoïdal
amplitude = 2.0  # Amplitude du signal en volts
frequency = 1000  # Fréquence du signal en Hz
sample_rate = 1000*frequency  # Taux d'échantillonnage (nombre de points par seconde)

# Générer les données du signal sinusoïdal
num_samples = sample_rate  # On génère un second de données
t = np.linspace(0, 1, num_samples, endpoint=False)  # Axe temporel pour 1 seconde
signal = amplitude * np.sin(2 * np.pi * frequency * t)  # Signal sinusoïdal

# Créer une tâche DAQ pour la sortie analogique
with nidaqmx.Task() as task:
    # Ajouter un canal de sortie analogique (par exemple 'Dev1/ao0' pour la sortie analogique 0)
    task.ao_channels.add_ao_voltage_chan("Dev1/ao0")

    # Configurer le taux d'échantillonnage en mode échantillonnage continu
    task.timing.cfg_samp_clk_timing(
        sample_rate,  # Taux d'échantillonnage
        sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS  # Mode continu
    )

    # Démarrer explicitement la tâche avant d'écrire des données
    task.write(signal, auto_start=False)

    # Commencer la génération
    task.start()

    try:
        print("Génération du signal en continu... Appuyez sur Ctrl+C pour arrêter.")
        while True:
            time.sleep(1)  # Maintenir la boucle infinie
    except KeyboardInterrupt:
        print("Génération interrompue par l'utilisateur.")
    finally:
        task.stop()  # Assurez-vous que la tâche s'arrête correctement
