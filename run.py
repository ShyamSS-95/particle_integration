from modules import *
from simulation_parameters import *

if(simulation_dimension == 2):
  sol = np.zeros(4*no_of_particles,dtype=np.float)
  old = np.zeros(4*no_of_particles,dtype=np.float)

if(simulation_dimension == 3):
  sol = np.zeros(6*no_of_particles,dtype=np.float)
  old = np.zeros(6*no_of_particles,dtype=np.float)

h5f                = h5py.File('data_files/initial_conditions/initial_data.h5', 'r')
initial_conditions = h5f['initial_conditions'][:]
time               = h5f['time'][:]
h5f.close()

dt = time[1]

"""Declaring data variables which shall be used in post-processing"""

momentum_x     = np.zeros(time.size)
momentum_y     = np.zeros(time.size)
kinetic_energy = np.zeros(time.size)
pressure       = np.zeros(time.size)
heatflux_x     = np.zeros(time.size)
heatflux_y     = np.zeros(time.size)

if(simulation_dimension == 3):
  momentum_z = np.zeros(time.size)
  heatflux_z = np.zeros(time.size)

if(collision_operator == 2):
  potential_energy = np.zeros(time.size)

# Now we shall proceed to evolve the system with time
for time_index,t0 in enumerate(time):
  
  print("Computing For Time Index = ",time_index)
  
  if(time_index == time.size-1):
    break
  
  if(time_index==0):
    initial_conditions = initial_conditions
  else:
    initial_conditions = old
  
  if(choice_integrator == 0):
    from integrators.verlet import integrator

  elif(choice_integrator == 1):
    from integrators.fourth_order_symplectic import integrator
  
  #pressure1 = np.sum(initial_conditions[3*no_of_particles:4*no_of_particles]**2+initial_conditions[4*no_of_particles:5*no_of_particles]**2+initial_conditions[5*no_of_particles:6*no_of_particles]**2)/no_of_particles
  #print(pressure1)
  sol = integrator(initial_conditions,dt)
  #pressure1 = np.sum(sol[3*no_of_particles:4*no_of_particles]**2+sol[4*no_of_particles:5*no_of_particles]**2+sol[5*no_of_particles:6*no_of_particles]**2)/no_of_particles
  #print(pressure1)
  
  if(wall_condition_x == 2):
    from wall_options.thermal_wall_x import wall_x
  elif(wall_condition_x == 1):
    from wall_options.hard_wall_x import wall_x
  elif(wall_condition_x == 0):
    from wall_options.periodic_x import wall_x

  if(wall_condition_y == 2):
    from wall_options.thermal_wall_y import wall_y
  elif(wall_condition_y == 1):
    from wall_options.hard_wall_y import wall_y
  elif(wall_condition_y == 0):
    from wall_options.periodic_y import wall_y

  sol = wall_x(sol)
  #pressure1 = np.sum(sol[3*no_of_particles:4*no_of_particles]**2+sol[4*no_of_particles:5*no_of_particles]**2+sol[5*no_of_particles:6*no_of_particles]**2)/no_of_particles
  #print(pressure1)
  sol = wall_y(sol)
  #pressure1 = np.sum(sol[3*no_of_particles:4*no_of_particles]**2+sol[4*no_of_particles:5*no_of_particles]**2+sol[5*no_of_particles:6*no_of_particles]**2)/no_of_particles
  #print(pressure1)
  
  if(simulation_dimension == 3):
    if(wall_condition_z == 2):
      from wall_options.thermal_wall_z import wall_z
    elif(wall_condition_z == 1):
      from wall_options.hard_wall_z import wall_z
    elif(wall_condition_z == 0):
      from wall_options.periodic_z import wall_z

    sol = wall_z(sol)
  
  old = sol

  """Declaring variables used in calculation for post-processor"""

  if(simulation_dimension == 2):
    x_coordinates = sol[0:no_of_particles]
    y_coordinates = sol[no_of_particles:2*no_of_particles] 
    velocity_x    = sol[2*no_of_particles:3*no_of_particles]
    velocity_y    = sol[3*no_of_particles:4*no_of_particles]

  if(simulation_dimension == 3):
    x_coordinates = sol[0:no_of_particles]
    y_coordinates = sol[no_of_particles:2*no_of_particles] 
    z_coordinates = sol[2*no_of_particles:3*no_of_particles]
    velocity_x    = sol[3*no_of_particles:4*no_of_particles]
    velocity_y    = sol[4*no_of_particles:5*no_of_particles]
    velocity_z    = sol[5*no_of_particles:6*no_of_particles]

  """Calculation of the functions which will be used to post-process the results of the simulation run"""

  if(simulation_dimension == 2):
    momentum_x[time_index]     = mass_particle * np.sum(velocity_x)
    momentum_y[time_index]     = mass_particle * np.sum(velocity_y)
    kinetic_energy[time_index] = 0.5*mass_particle*np.sum(velocity_x**2 + velocity_y**2)
    pressure[time_index]       = np.sum(velocity_x**2 + velocity_y**2)/no_of_particles
    heatflux_x[time_index]     = np.sum(velocity_x*(velocity_x**2 + velocity_y**2))/no_of_particles
    heatflux_y[time_index]     = np.sum(velocity_y*(velocity_x**2 + velocity_y**2))/no_of_particles

  if(simulation_dimension == 3):
    momentum_x[time_index]     = mass_particle * np.sum(velocity_x)
    momentum_y[time_index]     = mass_particle * np.sum(velocity_y)
    momentum_z[time_index]     = mass_particle * np.sum(velocity_z)

    kinetic_energy[time_index] = 0.5*mass_particle*np.sum(velocity_x**2 + velocity_y**2 + velocity_z**2)
    
    pressure[time_index]       = np.sum(velocity_x**2 + velocity_y**2 + velocity_z**2)/no_of_particles
    
    heatflux_x[time_index]     = np.sum(velocity_x*(velocity_x**2 + velocity_y**2 + velocity_z**2))/no_of_particles
    heatflux_y[time_index]     = np.sum(velocity_y*(velocity_x**2 + velocity_y**2 + velocity_z**2))/no_of_particles
    heatflux_z[time_index]     = np.sum(velocity_z*(velocity_x**2 + velocity_y**2 + velocity_z**2))/no_of_particles

  if(collision_operator == 2):
    from collision_operators.potential import calculate_potential_energy
    potential_energy = calculate_potential_energy(sol)

  print(pressure[time_index])
  
  # Writing the data to file every 1000 time steps
  # This data will then be post-processed to generate results
  
  if((time_index%1000)==0):
    h5f = h5py.File('data_files/timestepped_data/solution_'+str(time_index)+'.h5', 'w')
    h5f.create_dataset('sol',                data = sol)
    h5f.create_dataset('momentum_x',         data = momentum_x)
    h5f.create_dataset('momentum_y',         data = momentum_y)
    h5f.create_dataset('heatflux_x',         data = heatflux_x)
    h5f.create_dataset('heatflux_y',         data = heatflux_y)
    if(simulation_dimension == 3):
      h5f.create_dataset('heatflux_z',       data = heatflux_z)
      h5f.create_dataset('momentum_z',       data = momentum_z)
    h5f.create_dataset('kinetic_energy',     data = kinetic_energy)
    h5f.create_dataset('pressure',           data = pressure)
    if(collision_operator == 2):
      h5f.create_dataset('potential_energy', data = pressure)
    h5f.create_dataset('time',               data = time)
    h5f.close()