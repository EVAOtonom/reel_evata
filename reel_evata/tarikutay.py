#!/usr/bin/env python3.9

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8


class CmdVelSubscriber(Node):
    def __init__(self):
        super().__init__('cmd_vel_subscriber')

        # Publisher'ları tanımlıyoruz
        self.steering_angle_pub = self.create_publisher(Int8, '/stm/steering_angle', 10)
        self.motor_power_pub = self.create_publisher(Int8, '/stm/motor_power', 10)
        
        # /cmd_vel topiğine abone olma
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.listener_callback,
            10)
        
        self.get_logger().info('CmdVel Subscriber Node başlatıldı...')

    def listener_callback(self, msg):
        # Gelen Twist mesajından x-lineer ve z-açısal hızları alıyoruz
        linear_x = msg.linear.x
        angular_z = msg.angular.z
        
        # Direksiyon açısını hesapla (Int8 sınırlarını kontrol et)
        steering_value = int(angular_z * 80)
        steering_value = max(-128, min(127, steering_value))

        # Motor gücünü hesapla (Int8 sınırlarını kontrol et)
        motor_value = int(linear_x * 1)
        motor_value = max(-5, min(5, motor_value))
        
        # Yayınlanan mesajlar
        steering_msg = Int8()
        steering_msg.data = steering_value
        self.steering_angle_pub.publish(steering_msg)
        
        motor_msg = Int8()
        motor_msg.data = motor_value
        self.motor_power_pub.publish(motor_msg)

        # Debug log
        self.get_logger().info(
            f'Gelen Twist: linear_x={linear_x}, angular_z={angular_z} | Gönderilen: Steering={steering_value}, Motor={motor_value}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = CmdVelSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
