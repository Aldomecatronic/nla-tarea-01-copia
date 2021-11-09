#!/usr/bin/python3

import rospy
from geometry_msgs.msg import Twist
from rospy.timer import Rate
from std_msgs.msg import String



class MoveRobot():
    def __init__(self):
        self.mov_msg = Twist()
        self.mov_msg.linear.x = 0.0 # velocidad lineal
        self.mov_msg.angular.z = 0.0 # velocidad angular


        # Creando el publisher
        rospy.Subscriber('/recognizer/output', String, callback=self.mapea_movimiento) # Subscribes to the /recognizer/output topic


        # Creando el editor con el tipo de datos Twist
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1) # cmd_vel is the topic
        
        
        rate = rospy.Rate(1) # 1 Hz


        if rospy.on_shutdown(self.get_stop):
            print('Program execution is stopped')


        # A continuación escribe lo que quiere que se publique
        while not rospy.is_shutdown(): 
            self.pub.publish(self.mov_msg)
            print(self.mov_msg) # Shown on the console
            rate.sleep()  



    # Función que mueve el robot
    def mapea_movimiento(self, mov): 
        comando = mov.comando

        if(comando.lower() == 'avanza'):
            self.mov_msg.linear.x = 0.3
            self.mov_msg.angular.z = 0.0
        elif(comando.lower() == 'detente'):
            self.mov_msg.linear.x = 0.0
            self.mov_msg.angular.z = 0.0   
        elif(comando.lower() == 'gira'):
            self.mov_msg.linear.x = 0.0
            self.mov_msg.angular.z = 0.2
        else:
            print('¡Comando incorrecto!')

    # Función que se ejecuta cuando el programa se detiene
    def get_stop(self):
        self.mov_msg.linear.x = 0.0
        self.mov_msg.angular.z = 0.0
        msg = self.mov_msg
        print(msg)
        self.pub.publish(msg)
        
if __name__ == '__main__':
    rospy.init_node('action_pub', anonymous=True)
    print('Nodo creado')
    try:
        MoveRobot()
    except rospy.ROSInterruptException:
        pass