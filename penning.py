# URO Group 49
# 2015-03-20
# Charged Ion in TITAN Penning Trap (Animation)
# Prototype 6

# Changes made:
#   - Added ability to pause the program
#   - Added ability to increase/decrease animation rate during the program
#   - Can customize keys used to pause, increase, decrease
#   - Can customize amount of increase/decrease
#   - Time label adjusts to rate of animation
#   - Can edit rate while paused

# Possible future changes
#   - Create multiple test functions (in a class) and organize them
#   - Put together an alternate version of the program that is a stepper according to a numerical approximation
#   - Write a wx Applet that allows user to interact with program (i.e. specify initial conditions, restart, etc.)

# from __future__ import print_function
from visual import *

Pi = acos(-1)

# Ion image
ion_image_radius = 4
ion_color = color.red

# Ion trail
builtin_trail = True
trail_style = "points"
trail_retain = 1000000
trail_interval = 1
marker_size = 1.0
trail_color = color.white

# Axis
view_axis = True
view_axis_labels = True
arrow_color = trail_color
arrow_length_scale = .25  # Times R_minus
axis_width_scale = .02    # Times length

# Time
show_time = True

# Text
text_color = trail_color

# Scene specifications
height = 780
width = 1280
scene.title = 'Charged ion in TITAN Measurement Penning Trap'
scene.height = height
scene.width = width
scene.background = color.black

# Animation conditions
PAUSE = True
step_size = .000000005
num_steps = 1000000
duration = step_size*num_steps
loops_per_sec = 1500.0
rate_increase_amount = loops_per_sec/10.0
pause_key = 'p'
increase_key = 'right'
decrease_key = 'left'

# Initial conditions
initialPosition = vector(.001, .001, .001)             # m
initialVelocity = vector(300.0, 400.0, 50.0)          # m/s

# Animation
dimension_scale_factor = 100000.0

# Universal constants
amu = 1.66053892*10**(-27)  # kg
e = 1.602176565*10**(-19)   # C


class Ion:
    def __init__(self, mass, charge, description=""):
        self.m = abs(mass)
        self.q = charge
        self.id = description

proton = Ion(1.67262158*10**(-27), e, "Proton")
electron = Ion(9.10938291*10**(-31), -e, "Electron")
email = Ion(74*amu, 8*e, "Ion from Brian email")
Rb_85 = Ion(85*amu, e, "Rb 85")
Rb_87 = Ion(87*amu, e, "Rb 87")


class PenningTrap:
    def __init__(self, magnetic_field, static_voltage, characteristic_dimension=11.21*10**(-3), z_0=False, rho_0=False, description=""):
        self.B_0 = magnetic_field
        self.U_0 = static_voltage
        self.id = description
        if z_0 is not False and rho_0 is not False:
            self.d = sqrt(.5*(z_0**2 + .5 * rho_0**2))
        else:
            self.d = characteristic_dimension

# TITAN = PenningTrap(3.7, 35.75, description="TITAN", z_0=.01215, rho_0=.015)
TITAN = PenningTrap(3.7, 35.75, characteristic_dimension=11.21*10**(-3), description="TITAN")


class Setup:
    def __init__(self, penning_trap, ion, initial_position, initial_velocity, alt_voltage=False, alt_magnetic_field=False):
        self.pt = penning_trap
        self.ion = ion
        self.t = 0
        self.ion.s0 = initial_position
        self.ion.v0 = initial_velocity
        if alt_voltage is not False:
            self.pt.U_0 = alt_voltage
        if alt_magnetic_field is not False:
            self.pt.B_0 = alt_magnetic_field


        # Constants
        m = ion.m
        q = ion.q
        B_0 = self.pt.B_0
        U_0 = self.pt.U_0
        d = self.pt.d
        s0 = self.ion.s0
        v0 = self.ion.v0

        self.ion.s0_r = sqrt(s0.x**2 + s0.y**2)
        self.ion.s0_z = abs(s0.z)
        self.ion.v0_r = sqrt(v0.x**2 + v0.y**2)
        self.ion.v0_z = abs(v0.z)


        # Eigenfrequencies
        omega_c = q*B_0/m
        omega_z = sqrt(q*U_0/(m*d**2))
        omega_1 = sqrt(omega_c**2 - 2*omega_z**2)

        self.bounded = (omega_c**2 - 2*omega_z**2 > 0)

        omega_plus = .5*(omega_c + omega_1)
        omega_minus = .5*(omega_c - omega_1)

        self.omega_c = omega_c
        self.omega_plus = omega_plus
        self.omega_minus = omega_minus
        self.omega_z = omega_z


        # Amplitudes
        R_plus = sqrt((((q/abs(q))*v0.y + omega_minus*s0.x)**2 + (v0.x - (q/abs(q))*omega_minus*s0.y)**2) /
                      ((omega_minus - omega_plus)**2))
        R_minus = sqrt((((q/abs(q))*v0.y + omega_plus*s0.x)**2 + (v0.x - (q/abs(q))*omega_plus*s0.y)**2) /
                       ((omega_plus - omega_minus)**2))
        R_z = sqrt(s0.z**2 + (v0.z**2)/(omega_z**2))

        self.R_plus = R_plus
        self.R_minus = R_minus
        self.R_z = R_z


        # Phase constants
        phi_plus = acos(((q/abs(q))*v0.y + omega_minus*s0.x) / (R_plus*(omega_minus - omega_plus)))
        phi_minus = acos(((q/abs(q))*v0.y + omega_plus*s0.x) / (R_minus*(omega_plus - omega_minus)))
        phi_z = acos(s0.z/R_z)

        self.phi_plus = phi_plus
        self.phi_minus = phi_minus
        self.phi_z = phi_z

    # Time -> Float
    # Given time, produce the x-coordinate of the ion
    def get_x(self, time):
        t = time
        R_plus = self.R_plus
        R_minus = self.R_minus
        omega_plus = self.omega_plus
        omega_minus = self.omega_minus
        phi_plus = self.phi_plus
        phi_minus = self.phi_minus

        x_t = R_plus * cos(omega_plus * t + phi_plus) + R_minus * cos(omega_minus * t + phi_minus)
        return x_t

    # Time -> Float
    # Given time, produce the y-coordinate of the ion
    def get_y(self, time):
        t = time
        q = self.ion.q
        R_plus = self.R_plus
        R_minus = self.R_minus
        omega_plus = self.omega_plus
        omega_minus = self.omega_minus
        phi_plus = self.phi_plus
        phi_minus = self.phi_minus

        y_t = (-q/abs(q)) * (R_plus * sin(omega_plus * t + phi_plus) + R_minus * sin(omega_minus * t + phi_minus))
        return y_t

    # Time -> Float
    # Given time, produce the z-coordinate of the ion
    def get_z(self, time):
        t = time
        R_z = self.R_z
        omega_z = self.omega_z
        phi_z = self.phi_z

        z_t = R_z * cos(omega_z*t + phi_z)
        return z_t

    # Time -> Position
    # Given time, return position vector
    def get_position(self, time=False):
        if time is not False:
            t = time
        else:
            t = self.t

        x = self.get_x(t)
        y = self.get_y(t)
        z = self.get_z(t)

        s = vector(x, y, z)
        return s

    # Self -> Self
    # Add time step to current time
    def update_time(self):
        t_f = self.t + step_size
        self.t = t_f

    # Self -> Self
    # Update position based on current time
    def update_position(self):
        s_f = self.get_position()
        s_f *= dimension_scale_factor
        self.ion.s = s_f

    # Self -> Self
    # Print out information
    def printData(self):
        print "Ion:              " + self.ion.id
        print "M (kg) =          " + str(self.ion.m)
        print "Q (C) =           " + str(self.ion.q)
        print ""
        print "Initial conditions:"
        print "s0_r (m) =        " + str(self.ion.s0_r)
        print "s0_z (m) =        " + str(self.ion.s0_z)
        print "v0_r (m/s) =      " + str(self.ion.v0_r)
        print "v0_z (m/s) =      " + str(self.ion.v0_z)
        print ""
        print "Penning Trap:     " + self.pt.id
        print "U_0 (V) =         " + str(self.pt.U_0)
        print "B_0 (T) =         " + str(self.pt.B_0)
        print "d_0 (m) =         " + str(self.pt.d)
        print ""
        print "Eigenfrequencies:"
        print "omega_c (rad/s) = " + str(self.omega_c)
        print "omega_+ (rad/s) = " + str(self.omega_plus)
        print "omega_- (rad/s) = " + str(self.omega_minus)
        print "omega_z (rad/s) = " + str(self.omega_z)
        print ""
        print "Frequencies:"
        print "nu_c (Hz) =       " + str(self.omega_c/(2*pi))
        print "nu_+ (Hz) =       " + str(self.omega_plus/(2*pi))
        print "nu_- (Hz) =       " + str(self.omega_minus/(2*pi))
        print "nu_z (Hz) =       " + str(self.omega_z/(2*pi))
        print ""
        print "Radius:"
        print "R_+ (m) =         " + str(self.R_plus)
        print "R_- (m) =         " + str(self.R_minus)
        print "R_z (m) =         " + str(self.R_z)
        print ""
        print "Phase constants:"
        print "phi_+ (rad) =     " + str(self.phi_plus)
        print "phi_- (rad) =     " + str(self.phi_minus)
        print "phi_z (rad) =     " + str(self.phi_z)

setup1 = Setup(TITAN, email, initialPosition, initialVelocity)
setup2 = Setup(TITAN, proton, initialPosition, initialVelocity)
setup3 = Setup(TITAN, Rb_85, initialPosition, initialVelocity)
setup4 = Setup(TITAN, Rb_87, initialPosition, initialVelocity)


def initialize_animation(state):
    if state.bounded:
        # Print frequencies
        state.printData()

        # Get values
        T = []
        S = []
        for i in range(0, num_steps):
            t_i = i*step_size
            s_i = state.get_position(t_i)
            T.append(t_i)
            S.append(s_i)

        # Animate
        scaledS = []
        for i in range(0, num_steps):
            scaledS_i = S[i] * dimension_scale_factor
            scaledS.append(scaledS_i)

        s_0 = scaledS[0]
        t_0 = T[0]

        # Display axes
        if view_axis:
            arrow_length = state.R_minus*dimension_scale_factor*arrow_length_scale

            x_plus_axis = arrow(pos=vector(0.0, 0.0, 0.0),
                                axis=vector(arrow_length, 0.0, 0.0),
                                color=arrow_color,
                                shaftwidth=axis_width_scale*arrow_length)
            y_plus_axis = arrow(pos=vector(0.0, 0.0, 0.0),
                                axis=vector(0.0, arrow_length, 0.0),
                                color=arrow_color,
                                shaftwidth=axis_width_scale*arrow_length)
            z_plus_axis = arrow(pos=vector(0.0, 0.0, 0.0),
                                axis=vector(0.0, 0.0, arrow_length),
                                color=arrow_color,
                                shaftwidth=axis_width_scale*arrow_length)
            x_minus_axis = arrow(pos=vector(0.0, 0.0, 0.0),
                                 axis=vector(-arrow_length, 0.0, 0.0),
                                 color=arrow_color,
                                 shaftwidth=axis_width_scale*arrow_length)
            y_minus_axis = arrow(pos=vector(0.0, 0.0, 0.0),
                                 axis=vector(0.0, -arrow_length, 0.0),
                                 color=arrow_color,
                                 shaftwidth=axis_width_scale*arrow_length)
            z_minus_axis = arrow(pos=vector(0.0, 0.0, 0.0),
                                 axis=vector(0.0, 0.0, -arrow_length),
                                 color=arrow_color,
                                 shaftwidth=axis_width_scale*arrow_length)

            if view_axis_labels:
                x_label = label(text="x",
                                pos=(x_plus_axis.axis.x+5, 0, 0),
                                box=false,
                                height=10,
                                font='monospace',
                                color=arrow_color,
                                opacity=0)
                y_label = label(text="y",
                                pos=(0, y_plus_axis.axis.y+5, 0),
                                box=false,
                                height=10,
                                font='monospace',
                                color=arrow_color,
                                opacity=0)
                z_label = label(text="z",
                                pos=(0, 0, z_plus_axis.axis.z+5),
                                box=false,
                                height=10,
                                font='monospace',
                                color=arrow_color,
                                opacity=0)

        if builtin_trail:
            ion_image = sphere(pos=s_0,
                               rad=ion_image_radius,
                               color=ion_color,
                               make_trail=true,
                               trail_type=trail_style,
                               interval=trail_interval,
                               retain=trail_retain)
            ion_image.trail_object.color = trail_color
            ion_image.trail_object.size = marker_size
        else:
            ion_image = sphere(pos=s_0,
                               radius=ion_image_radius,
                               color=ion_color)

        # Display time
        if show_time:
            ppd_ts = int(abs(log10(step_size)))
            time_string = "t = "+"%1."+str(ppd_ts)+"f"+" s"

            real_time = step_size*loops_per_sec
            ppd_rt = int(abs(log10(real_time)) + abs(log10(loops_per_sec/rate_increase_amount)))
            real_time_str = "%1."+str(ppd_rt)+"f"+" x Real Time"

            str1 = real_time_str % real_time
            str2 = time_string % t_0
            time_label = label(text=str1+"\n"+str2,
                               xoffset=-.35*width,
                               yoffset=.35*height,
                               line=0,
                               box=false,
                               height=10,
                               font='monospace',
                               color=text_color)

        i = 0
        while True:
            rate(loops_per_sec)

            if i < num_steps:
                # Update time label
                if show_time:
                    t_i = T[i]
                    real_time = step_size*loops_per_sec

                    str1 = real_time_str % real_time
                    str2 = time_string % t_i
                    time_label.text = str1+"\n"+str2

                if PAUSE:
                    continue

                s_i = scaledS[i]
                ion_image.pos = s_i

                i += 1
            else:
                break

        # print(scaledS[:100], sep='\n')
    else:
        print("The ion's motion is not bounded; adjust parameters")


def handle_keys(evt):
    global PAUSE
    global loops_per_sec

    s = evt.key

    if s == pause_key:
        if PAUSE:
            PAUSE = False
        else:
            PAUSE = True

    if s == decrease_key:
        if loops_per_sec > rate_increase_amount:
            loops_per_sec -= rate_increase_amount
    elif s == increase_key:
        loops_per_sec += rate_increase_amount

scene.bind('keydown', handle_keys)

initialize_animation(setup3)
