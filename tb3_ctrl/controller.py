import rclpy
from rclpy.node import Node
from geometry_msgs.msg._twist import Twist
import curses
from curses import wrapper

class ControllerPublisher(Node):
    def __init__(self):
        super().__init__("controller_publisher")
        self.publisher_ = self.create_publisher(Twist, "/cmd_vel", 10)
        
    def controller(self, stdscr):
        twist = Twist()
        
        # Create static info menu
        stdscr.clear()
        stdscr.addstr(0, 0, "-----------------------------")
        stdscr.addstr(1, 0, "Moving around:")
        stdscr.addstr(2, 0, "Control your turtlebot3!")
        stdscr.addstr(3, 0, "       w      ")
        stdscr.addstr(4, 0, "   a   s   d  ")
        stdscr.addstr(5, 0, "       x      ")
        stdscr.addstr(6, 0, " ")
        stdscr.addstr(7, 0, "w/x: increase linear velocity")
        stdscr.addstr(8, 0, "a/d: increase angular velocity")
        stdscr.addstr(9, 0, "s: stop")
        stdscr.addstr(10, 0, " ")
        stdscr.addstr(11, 0, "Press Ctrl C to exit")
        stdscr.move(12, 0)
        stdscr.refresh()
        
        # Create window with updating movement info
        
        output_win = curses.newwin(0, 0, 12, 0)
        
        while True:
            try:
                input = stdscr.getkey()
                match input:
                    case "w":
                        twist.linear.x += 0.1
                        output_win.clear()
                        output_win.addstr(f"currently:   lv: {round(twist.linear.x, 4)}  av: {round(twist.angular.z, 4)}")
                        output_win.refresh()
                    case "a":
                        twist.angular.z += 0.1
                        output_win.clear()
                        output_win.addstr(f"currently:   lv: {round(twist.linear.x, 4)}  av: {round(twist.angular.z, 4)}")
                        output_win.refresh()
                    case "s":
                        twist.linear.x = 0.0
                        twist.angular.z = 0.0
                        output_win.clear()
                        output_win.addstr(f"currently:   lv: {round(twist.linear.x, 4)}  av: {round(twist.angular.z, 4)}")
                        output_win.refresh()
                    case "d":
                        twist.angular.z -= 0.1
                        output_win.clear()
                        output_win.addstr(f"currently:   lv: {round(twist.linear.x, 4)}  av: {round(twist.angular.z, 4)}")
                        output_win.refresh()
                    case "x":
                        twist.linear.x -= 0.1
                        output_win.clear()
                        output_win.addstr(f"currently:   lv: {round(twist.linear.x, 4)}  av: {round(twist.angular.z, 4)}")
                        output_win.refresh()  
                        
            except KeyboardInterrupt:
                twist.linear.x = 0.0
                twist.angular.z = 0.0
                break
            
            self.publisher_.publish(twist)
        
        
def main(args=None):
    rclpy.init(args=args)
    
    ctrl_pub = ControllerPublisher()
    wrapper(ctrl_pub.controller)
    
    ctrl_pub.destroy_node()
    

if __name__ == "__main__":
    main()