# fichier: send_constant_voltage.py
import nidaqmx
import time

# Paramètres du signal
ao1_constant_voltage = 5  # Tension constante à envoyer en volts
ao2_constant_voltage = 2.5 

# Configuration de la tâche d'écriture pours envoyer une tension constante
with nidaqmx.Task() as write_task:
    write_task.ao_channels.add_ao_voltage_chan("Dev1/ao0")
    write_task.ao_channels.add_ao_voltage_chan("Dev1/ao1")

    # Envoi de la tension constante en continu
    print(f"Envoi d'une tension constante de {ao1_constant_voltage}V sur ao0. Appuyez sur Ctrl+C pour arrêter.")
    print(f"Envoi d'une tension constante de {ao2_constant_voltage}V sur ao1. Appuyez sur Ctrl+C pour arrêter.")

    try:
        while True:
            write_task.write([ao1_constant_voltage, ao2_constant_voltage])  # Envoie la tension constant
            time.sleep(1)  # Pause pour éviter la surcharge du processeur
    except KeyboardInterrupt:
        print("Envoi de la tension interrompu.")
