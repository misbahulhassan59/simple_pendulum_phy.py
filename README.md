# simple_pendulum_phy.py

Simple Pendulum Physics



Introduction:  A code has been designed using python libraries which takes mass of the bob, length of the pendulum,initial angle of the bob 
and initial angular velocity as input from user to derive the differential equation of the simple pendulum system, draw 3 graphs (angle vs 
time, angular velocity vs time and phase space) and finally simulates the motion of simple pendulum.

Note: You need to cancel the graphs first and then the simulation wil appear. Also, the code will run in terminal in visual studio due to'input()'

Discussion:

part(1) (importing essential libraries or libraries' files):

1  import numpy as np
2  import matplotlib.pyplot as plt
3  from scipy.integrate import odeint
4  from matplotlib import animation
5  import matplotlib.patches as patches
6  import sympy as sym


Here some libraries etc which will be used many times are given short names while others which are used once or twice are left out
-'numpy' is a library used to evaluate mathematical formulas i.e but numbers inside it to extract a number 
-'scipy' is a library whose 'integrate' file contains a function named 'odient' which solves differential eqs 
-'sympy'is a library which is used to create symbolic variables i.e varaibles of which simple algebra works and perform other things discussed later
-'matplotlib'is a library from which three things are imported: 1st is 'pyplot' (for drawing graphs), 2nd is 'animation'(for animation)
and 3rd is 'patches' for drawing shapes like circle etc.


part(2)  symbolic variables:

7  g = sym.symbols('g')
8  l = sym.symbols('l')
9  m = sym.symbols('m')
10 t = sym.symbols('t')

-'g' is the gravitational acceleration
-'l' is the length of simple pendulum
-'m' is the mass of the bob
-'t' is the time for which the simulation occurs
Here a function called 'symbols()' from sym (i.e short of sympy) is used to convert the string names into symbolic variables i.e varables on which 
simple algebric simplifcations can be performed 
example: x*x is conveted to x^2 without error if x is symbolic variable

11  theta = sym.symbols('\u03B8', cls=sym.Function)
12  theta = theta(t)

-'theta' is the angle the simple pendulum makes with the mean postion at any instant
Here in line 11 'theta' is introduced using the same 'symbols()' but is created as a function. '\u03B8' is the Unicode Escape Sequence for greek letter
theta and in 'cls=sym.Function', cls is the class. so you are going inside 'sym' and taking the class 'Function' and attributing it to theta.
then is line 12 it is explicitly made a function of 't' i.e angle depends on time.

part(3) (Physics, Maths and Langrangian Mechanics):

13  x = l * sym.sin(theta)
14  y = -l * sym.cos(theta)

Here 'x' and 'y' two sym objects are introduced ,representing the coordinates the bob the bob at any instant. these formulas are derived from trignometry.
'sym.sin(theta)' and 'sym.cos(theta)' are two functions taken from 'sym' which are just the algebric sine and cosine functions depending on the angle 
of the pendulum at any instant. this means 'x' and 'y' are constant symbolic objects but depend on 't'.
Note: The -ve sign ensures the whole pendulum is below the x-axis.

16  T = sym.Rational(1, 2) * m * (x.diff(t) ** 2 + y.diff(t) **2)

Here 'T' represents kinetic energy of the bob at any instant (1/2)*m*v^2.
-'sym.Rational(1, 2)' ,Rational() is a function inside 'sym' which ensures that python keeps fractions as fractions and doesn't convert them to floats.
the reason behind this is that sometimes while converting to fractions python rounds off the number introducing small errors. now, in this case it 
converts '1,2' to '1/2'
-'(x.diff(t) ** 2 + y.diff(t) **2)' , this is just the square of velocity written as the sum of squares of its vector components. In physics the 
same can be written as v^2=(dx/dt)^2 + (dy/dt)^2  . Here 'diff' is a thing from 'sym' that differentiates a symbolic object. One sytax to use this is:
object.diff(variable) ,where object is the thing to be differentiated and varirable is the thing with respect to which it should be differentiated 
(in this case it's 't').

19  V = m * g * y

Here 'V' is the potential energy of bob at any instant, 'm' is the mass and 'y' is the y-cooredinat eof bob

20  L = T - V
Here L is called Langrangian which is the difference of kinetic and potential energies of the object at any instant. it is from Lagrangian mechanics.

part (4) (deriving the differential equation of the simple pendulum using Langrian mechanics):

22  LE = (sym.diff(sym.diff(L, sym.diff(theta, t)), t) - sym.diff(L, theta)).simplify()

-'sym.diff(sym.diff(L, sym.diff(theta, t)), t) - sym.diff(L, theta)' is the python representation of left side of Lagrange equation (one can find it on internet, its difficult to write here). 
-'simplify()' , this is bult-in function in sym that simplifies algebric or trignometric expressions. For example (x^2-4)/(x+2) is simplified to (x-2).
In this case the formula for 'T' and 'V' are put inside 'L' and then are inserted directly into left side of Langrange equation. the derivaitves are taken, resulting in an ugly expression 'ml2θ¨-(-mglsinθ=0)' which can be simplified to 'ml2θ¨+mglsinθ'  by using 'simplify()'. 
-LE is the object in which this simplified expresson is stored.

23  sol = sym.solve(LE, sym.diff(theta, t, t), simplify=False, rational=False)

Here 'solve()' is a function that solves the input expression (1st parameter) by putting it equal to zero (ml2θ¨+mglsinθ=0) and represents the final formula by taking the specified varaible (2nd parameter) on one side (θ¨=−lg​sinθ) . Here simplification is prevented using 'simplify=False' (3rd thing) and rational number representation is prevented by 'rational=False' (4th thing) to speed up the calculations, because simplication takes time and rational forms are not useful for the 'odient' function which wil be used in future.
The return value of 'solve()' is a list whether its a single solution expression or multiple solution expressions so 'sol' stores a list.
in this case the solution is single algebric expression (not number!) and 'sol' represents 'θ¨' or 'angular acceleration'

27  print("\n\ndifferential equation of simple pendulum system:")
28  print("\u03B1=",sol[0],'\n')

in line 28 '\u03B1' is the Unicode Escape Sequence for alpha (angular acceleration or theta double dot) and 'sol[0]' is the first and the only element of the list stored in 'sol'. 
in short line 28 prints the famous simplified differential equation of simple pendulum.

part(5) (creating an array for storing the angles and their corresponding angular velocities evaluated from 'sol')

30  sol_f = sym.lambdify((t, theta, sym.diff(theta, t), g, l, m), sol[0])

-'lambdify()' is a function that creates a function 'sol_f' which converts symbolic expressions into 'numpy' form so that they can be evaluated easily. 
-'(t, theta, sym.diff(theta, t), g, l, m)' , the things inside 1st bracket are the input parameters. 'sym.diff(theta, t)' is angular velocity.
-'sol[0]' is the expression which should be evaluated and whose final value must be returned.
Here the function 'sol_f' evalutes the angular acceleration for particular inputs. 

31  def dSdt(S, t, g, l, m):
32      theta, omega = S
33  	dtheta_dt = omega
34  	domega_dt = sol_f(t, theta, omega, g, l, m)
35  	return dtheta_dt, domega_dt
36  t = np.linspace(0, 50, 2001)
37
38  theta0_deg = float(input("Enter inital angle (in degrees): "))
39  theta0 = np.deg2rad(theta0_deg)   # convert to radians
40
41  theta_dot0 = float(input("Enter initial angular velocity (rad/s): "))
42  g = 9.81
43  l = float(input("Enter length of pendulum (in meters): "))
44  m = float(input("Enter mass of pendulum (in kg): "))
45  ans = odeint(dSdt, (theta0, theta_dot0), t, args=(g, l, m))
  
Note: this is a difficult part. so i will not explain it in sequence of the code written but instead in the sequence of the logic through which code works

LOGIC:  
-Step 1: TIME IS DIVIDED
	 t = np.linspace(0, 50, 2001)
	 Here 'linspace()' is a function in 'np' that sets the starting, ending and interval length of a variable.Here 0 represents the starting value, 50 		 represents the ending value & '2001' represents the number of times stops will occur (i.e 2000 equal intervals).
	 dividing the time into large intervals is important. it serves many purposes like in plotting graphs and most importantly evaluating the theta and 	 	 angular velocity at these times.
-Step 2: user inputs are taken: 
	-theta0_deg = float(input("Enter inital angle (in degrees): "))
	 theta0 = np.deg2rad(theta0_deg)
         Here the user can enter the initial anlge in degrees which will be converted to radians using the 'deg2rad(theta0_deg)' function of 'np' 
	-theta_dot0 = float(input("Enter initial angular velocity (rad/s): "))
	 Here inital angular veocity can be entered
	-g = 9.81
	 Here the value of 'g' is fixed 
	-then 'l' and 'm' can be entered
-Step 3: ODIENT FUNCTION:
	 ans = odeint(dSdt, (theta0, theta_dot0), t, args=(g, l, m))
         although it is the last step but it should be logically analyzed first. Here 'odient()' is buuilt-in function in 'scipy' library that          solves differential equations. inside brackets:
		-dSdt 
		its a function which will be run again and again (for loop) for all 't' values. 'odient' is designed in such a way that the function calling 		is built inside it.
		-'(theta0, theta_dot0)' is called state (later represented as 'S').it's the tuple of variables whose values change. in the begining the 		  inital values are given. the odient names this tuple a state and assigns it to the first paramater of dSdt function, namely 'S'
		-'t' (3rd) is the thing which determines how many times 'odient' will call 'dSdt'
		-'args=(g, l, m)' , here 'arg' stands for arguments i.e constant varaibles for this function.
	 Note: the sequence of varaibles is important because it should be same as the dSdt function parameter sequence
-Step 4: dSdt FUNCTION:
	 def dSdt(S, t, g, l, m):
         	theta, omega = S
       	 	dtheta_dt = omega
 	 	domega_dt = sol_f(t, theta, omega, g, l, m)
 	 	return dtheta_dt, domega_dt
	 -the value of 'S' is given by 'odient' during calling
	 -theta, omega = S
	  here the 1st (theta0) and 2nd (theta_dot0) enteries of tuple 'S' are assigned to 'theta' and 'omega' respectively.
	 -dtheta_dt = omega
	  Here 'omega' is stored in another variable
	 -domega_dt = sol_f(t, theta, omega, g, l, m)
	  Here another function i.e the old 'sol_f' function is called to evaluate angular acceleration for a particular combination of variables and time 	  't'
	 -in the end angular velocity and angular accelerations are returned to 'odient' which stores angular velocity only and after using angular           accelration for next time value , it discards it.
Step 5 BACK TO ODIENT:
	 in the end 'odient' stores theta and angular velocity for each time value/loop iteration inside the row of a 2D array 'ans' consisting of two 	 columns. The value sof next iteration are stored in next row. therefore the 1st column 'ans' represents theta values for all times and the 2nd 	 column represents angular velocites for all times
          ans=|θ0       ω0      |
              |θ1       ω1	|
              |​​θ2	​​ω2	|
	      |​⋮​​		​​​⋮	|
	      |θ2000    ω2000​​	|


part (6)   (The graphs of angle vs time & angular velocity vs time) 

48  fig, ax = plt.subplots(1, 1, figsize=(11, 11))
49  ax.plot(t, ans[:, 0])
50  ax.set_xlabel('Time (s)')
51  ax.set_ylabel('Angle (rad)')

Here 'subplots()' is a function in 'plt' which is taking three things as parameter the number of rows on whole canvas, the number of columns on whole canvas, and figure size in sequence. The 'figsize' is given 11 by 11 inches size. the difference between various sizes can only be noticed when the graphs initially pop up and ot when they fill hte complete window. This reurns two things. 
the first things is stored in 'fig' which represents the whole canvas and not just graph. the second is 'ax' serves as array (not in this case) 
to store the number of rows and columns in which the cnavas is  divided.
line 49 plots the graph with 't' (the 1st argument) on x-axis and 'ans[:, 0]' on y-axis. in 'ans[:, 0]' the colon represents that you have to take all values and 0 represents the 0th column (theta/angle) 
finally, 50 and 51 labels the two axes

52  fig, bx = plt.subplots(1, 1, figsize=(11, 11))
53  bx.plot(t, ans[:, 1])
54  bx.set_xlabel('Time (s)')
55  bx.set_ylabel('Angular velocity (rad/s)')

this has the same procedure as above. it just plots angular velocity vs time.


part (7)  (the phase space graph):

57  fig, ax = plt.subplots(1, 1, figsize=(10, 5))
58  x_values, y_values = np.meshgrid(np.linspace(-10, 10, 20), np.linspace(-10, 10, 20))
59  u_values = y_values
60  v_values = -g/l * np.sin(x_values)
61  ax.streamplot(x_values, y_values, u_values, v_values)
62  ax.set_xlabel('Angle (rad)')
63  ax.set_ylabel('Angular velocity (rad/s)')
64  ax.grid()
65  plt.show()

line 57 already discussed. Here the normal plotting technique is not used. instead a meshgrid is introduced first using 'meshgrid()' from 'np' with two parameters for the range of axes of the grid. 'np.linspace()' has already been explained. 
lines 59 & 60 donot use 'ans' but instead they use a different technique to get variables. the x_coordinates are independent and can be used to represent theta. y_coordinates are also independent so can be used to represent angular velocity. together these two represent the axis of the grid. 
 'y_values' are also stored in another varaible 'u_values'. whereas v_values'store angular acceleration for each input x value(i.e theta) using the orignal formula that has been derived.
these four variables are used as paramters of the 'stream.plot()' to represent x_coordinates(in this case angle),y_coordinates(angular velocity), velocity in x direction (angular velocity) and velocity in y direction respectively (angular acceleration)
lines 62-63 label the axes , line 64 shows or prints the grid while line 65 shows all graphs.


part (8) (animation):
-the 1st functiion
66 def get_x_y(theta, l):
67  x = l * np.sin(theta)
68  y = -l * np.cos(theta)
69  return x, y

its a function that takes angle and length as input and returns the x and y corrdinates of the bob at all angles

-drawing grid:

72  fig, ax = plt.subplots(figsize=(5, 5))
73  ax.set_xlim(-l-1, l+1)
74  ax.set_ylim(-l-1, l+1)
75  ax.set_aspect('equal')
76  ax.grid()

line 72 is aready explained. while the lines 73 and 74 sets the limits of the axis according to the pendulum legth entered by user. line 75 keeps the same scale on both axes even when the graph is manifyed. Line 76 shows the grid

- Drawing line
78  line, = ax.plot([], [],'-', lw=2,color= 'brown')

the 'ax' created above is used to plot a graph i.e a line segment. the comma after 'line' forces the plot function to return only the first element of the list in non-list form
'[], []' are empty brackets which will change in future, containing corrdinates of bob. they also tell the plot to draw graph between origin and this point.
'-' draws a line, 'lw' determines the width & 'color= 'brown' determine sthe color of line. 

-drawing bob
79  bob = patches.Circle((0, 0), 0.09, fc='grey', ec='grey', zorder=3)
80  ax.add_patch(bob)

these two lines create a bob and adds it to ax 'ax'. the bob beignes at (0,0) but will adjust itself later on to the end of line

-text box for time
81  time_template = 'time = %.1fs'
82  time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

These two lines create a text box on graph for showing time, and adjust its position on the graph .'' is empty now it will change later on.

85  x, y = get_x_y(ans[:, 0], l)

Here 'get_x_y()' is called with the two paramters requuired to calculated the x and y coordinates of bob.

-the 2nd function:

87  def init():
88      line.set_data([], [])
89      time_text.set_text('')
90      bob.center=(0,0)
91      return line,bob, time_text
 this function initializes the line data set, the time reading and at the bob center so that no extra things appear and for clear apperance.

-the 3rd function 
92  def animate(i):
93      thisx = [0, x[i]]
94      thisy = [0, y[i]]
95      bob.center = (x[i], y[i])
96      line.set_data(thisx, thisy)
97      time_text.set_text(time_template % (i * t[1]))
98      return line,bob, time_text

line 93,94,96 adjus the end points of line encomassing the changes. line 95 moves the move. line 97 ensures time changes smoothly dependng on previous value. finally these three things are returned.

-the final step
101  ani = animation.FuncAnimation(fig, animate, np.arange(1, len(ans)),
                                interval=25, blit=True, init_func=init)

102  plt.rcParams['animation.embed_limit'] = 100
103  plt.show()

here the final naimatiion is created using the 'animation'.






	 








