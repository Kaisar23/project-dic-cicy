import cv2
import numpy as np
import multiprocessing
from harvesters.core import Harvester

def image_acquisition(serial_number):

    h = Harvester()
    h.add_file(r'C:\Users\Kaisa\Downloads\Baumer_GAPI_SDK_2.12.3_win_x86_64_c\bin\bgapi2_gige.cti')
    h.update()

    #print(h.device_info_list)

    ia = h.create({'serial_number':serial_number}) #Cámara derecha
    ia.start()
    ia.remote_device.node_map.ExposureTime.value = 350000

    #print(dir(ia.remote_device.node_map))

    while True:
        with ia.fetch() as buffer:
            component = buffer.payload.components[0]
            print(buffer.payload.components)
            _2d = component.data.reshape(component.height, component.width, int(component.num_components_per_pixel))
            frame = cv2.cvtColor(_2d, cv2.COLOR_GRAY2BGR)
            frame = cv2.resize(frame, (int(np.shape(frame)[1]/4), int(np.shape(frame)[0]/4)))
            cv2.imshow("Test", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    ia.stop()
    ia.destroy()

if __name__ == "__main__":

    serial_number_izq = "0599171415"
    serial_number_der = "0599371415"

    t1 = multiprocessing.Process(target = image_acquisition, args = (serial_number_izq,))
    t2 = multiprocessing.Process(target = image_acquisition, args = (serial_number_der,))

    t1.start()
    t2.start()

    #t1.join()
    #t2.join()