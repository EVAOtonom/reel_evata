#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class OdometerListener(Node):
    def __init__(self):
        super().__init__('odometer_listener')
        self.subscription = self.create_subscription(
            bool,
            '/stm/brake_status',
            self.listener_callback,
            10
        )
 # Gereksiz uyarıyı önler

    def listener_callback(self, msg):
        self.get_logger().info(f'Odometri Verisi: {msg.data:} cm')

def main(args=None):
    rclpy.init(args=args)
    node = OdometerListener()
    rclpy.spin(node)
