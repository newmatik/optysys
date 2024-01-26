import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import * 
import pygame
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        pygame.init()
        self.setWindowTitle("My App")
        self.layout = QGridLayout()


        self.setFixedSize(QSize(1000, 800))


        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_button_clicked)

        self.layout.addWidget(self.start_button)

        self.joystick_label = QLabel("Joystick")
        self.joystick_label.hide()
        self.layout.addWidget(self.joystick_label)




        
        self.row_headers = ['power',"Motor Jog X", "Motor Jog Y", "Motor Step left", "Motor Step right", "Motor Step up", "Motor Step down", "Zoom in", "Zoom out", "Focus near", "Focus far","Centering", "MODE","Zoom in Max", "Zoom out Max"]#
        self.table = QTableWidget(len(self.row_headers),2)
        self.table.setHorizontalHeaderLabels(["Joystick", "value"])
        for i,r in enumerate(self.row_headers):
            item = item = QTableWidgetItem(r)
            self.table.setItem(i, 0, item)
        # Adding the table to the layout
        self.layout.addWidget(self.table)
        self.table.hide()



        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)
    

    def start_button_clicked(self):
        print("Start button clicked")
        self.start_button.hide()
        self.joystick_label.show()
        self.table.show()
        self.show_joystick()


    def show_joystick(self):
        print("show_joystick")
        
        
        # Loop until the user clicks the close button.
        done = False
        flag_zoom_focus = True # True for zoom, False for focus
        Zoom_in = -1 
        Zoom_out = -1

        focus_near = 0
        focus_far = 0

        flag_zoom_focus = True # True for zoom, False for focus
        flag_stop_focus = True
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # Initialize the joysticks
        pygame.joystick.init()

        # -------- Main Program Loop -----------
        print("starting looop")
        while not done:

            # EVENT PROCESSING STEP
            for event in pygame.event.get():
                
                
                joystick = pygame.joystick.Joystick(0)
                joystick.init()
                power_level = joystick.get_power_level()
                item = QTableWidgetItem(str(power_level))
                idx = self.row_headers.index("power")
                self.table.setItem(idx, 1, item)
                

                # Motor Commands
                if joystick.get_button(5) == 1:
                    done = True
                
            

                
                if joystick.get_button(15) == 1:
                    item = QTableWidgetItem(str(1))
                    idx = self.row_headers.index("Centering")
                    self.table.setItem(idx, 1, item)
                else:
                    item = QTableWidgetItem(str(0))
                    idx = self.row_headers.index("Centering")
                    self.table.setItem(idx, 1, item)

                # step left
                if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(13) == 1:
                    item = QTableWidgetItem(str(1))
                    idx = self.row_headers.index("Motor Step left")
                    self.table.setItem(idx, 1, item)
                else:
                    item = QTableWidgetItem(str(0))
                    idx = self.row_headers.index("Motor Step left")
                    self.table.setItem(idx, 1, item)

                # step right
                if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(14) == 1:
                    item = QTableWidgetItem(str(1))
                    idx = self.row_headers.index("Motor Step right")
                    self.table.setItem(idx, 1, item)
                else:
                    item = QTableWidgetItem(str(0))
                    idx = self.row_headers.index("Motor Step right")
                    self.table.setItem(idx, 1, item)

                # step up
                if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(11) == 1:
                    item = QTableWidgetItem(str(1))
                    idx = self.row_headers.index("Motor Step up")
                    self.table.setItem(idx, 1, item)
                else: 
                    item = QTableWidgetItem(str(0))
                    idx = self.row_headers.index("Motor Step up")
                    self.table.setItem(idx, 1, item)


                # step down
                if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(12) == 1:
                    item = QTableWidgetItem(str(1))
                    idx = self.row_headers.index("Motor Step down")
                    self.table.setItem(idx, 1, item)
                else:
                    item = QTableWidgetItem(str(0))
                    idx = self.row_headers.index("Motor Step down")
                    self.table.setItem(idx, 1, item)

                # get values for jogging
                if abs(joystick.get_axis(0))>=0.1:#or joystick.get_axis(0)<-0.1) :
                    X = round(joystick.get_axis(0),1)*2
                else :
                    X = 0
                if abs(joystick.get_axis(1))>=0.1: # or joystick.get_axis(1)<-0.1) :
                    Y = round(joystick.get_axis(1)*(-1),1)*2 #(-20)
                else :
                    Y = 0
                item = QTableWidgetItem(str(X))
                idx = self.row_headers.index("Motor Jog X")
                self.table.setItem(idx, 1, item)
                item = QTableWidgetItem(str(Y))
                idx = self.row_headers.index("Motor Jog Y")
                self.table.setItem(idx, 1, item)


                # Camera commands
                if flag_zoom_focus:
                    # ZOOM MODE
                    focus_near = 0
                    focus_far = 0

                    if event.type == pygame.JOYAXISMOTION:
                        if joystick.get_axis(5)> -0.9:#or joystick.get_axis(0)<-0.1) :
                            val = round(joystick.get_axis(5),1)#
                            Zoom_in = val
                            # Zoom_in = map_decimal_to_integer(val)#1
                            
                        else :
                            Zoom_in = -1

                        if joystick.get_axis(4)>-0.9: # or joystick.get_axis(1)<-0.1) :
                            val = round(joystick.get_axis(4),1)
                            Zoom_out = val
                            # Zoom_out = map_decimal_to_integer(val)
                        else: 
                            Zoom_out = -1
                    
                else :
                    # FOCUS MODE 
                    Zoom_out = -1
                    Zoom_in = -1

                    if joystick.get_axis(4)> -0.9:
                        focus_far = 1
                    else :
                        focus_far = 0

                    if joystick.get_axis(5)>-0.9: 
                        focus_near = 1
                    else :
                        focus_near = 0
                item = QTableWidgetItem(str(Zoom_in))
                idx = self.row_headers.index("Zoom in")
                self.table.setItem(idx, 1, item)
                item = QTableWidgetItem(str(Zoom_out))
                idx = self.row_headers.index("Zoom out")
                self.table.setItem(idx, 1, item)
                item = QTableWidgetItem(str(focus_near))
                idx = self.row_headers.index("Focus near")
                self.table.setItem(idx, 1, item)
                item = QTableWidgetItem(str(focus_far))
                idx = self.row_headers.index("Focus far")
                self.table.setItem(idx, 1, item)

                        
                # Zoom in max 
                if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(10) == 1:
                    item = QTableWidgetItem(str(1))
                    idx = self.row_headers.index("Zoom in Max")
                    self.table.setItem(idx, 1, item)
                else:
                    item = QTableWidgetItem(str(0))
                    idx = self.row_headers.index("Zoom in Max")
                    self.table.setItem(idx, 1, item)
                # Zoom out max
                if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(9) == 1:
                    item = QTableWidgetItem(str(1))
                    idx = self.row_headers.index("Zoom out Max")
                    self.table.setItem(idx, 1, item)
                else:
                    item = QTableWidgetItem(str(0))
                    idx = self.row_headers.index("Zoom out Max")
                    self.table.setItem(idx, 1, item)
                
                # # toggle modes between focus and zoom
                if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(6) == 1:
                    flag_zoom_focus = not flag_zoom_focus

                if flag_zoom_focus:
                    item = QTableWidgetItem("Zoom")
                    idx = self.row_headers.index("MODE")
                    self.table.setItem(idx, 1, item)
                else:
                    item = QTableWidgetItem("Focus")
                    idx = self.row_headers.index("MODE")
                    self.table.setItem(idx, 1, item)
                    
        if done:
            exit()

        
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()