
class Molecule(object):
  """ Holds all the molecules. 

      Class atributes:
        give list

      Object attrubutes of each molecule used to determine where and how it is represented in the plot:
        1. positon: denotes placement in the left to right ordering of molecule
        2. name: moolecule name printed in plot; also acts as the key for molecule dictionary
        3. energy: relative energy of molecule; sets y-coordinate of line in plot
        4. excited: list denoting if molecule is excited state, and which surface it is on
        5. linecolor: color of the line in the plot
        6. linewidth: how bold the molecule's line is in the plot
        7. linethickness: how wide the line is from left to right
        8. x1 and x2: x-coordinates of the line in the plot
        9. name_font_size: obvious
       10. energy_font_size: obvious
  """

  molec_dict = {}   # Dictionary to store each of the molecule objects
  
  energy_list = []  # LIst of molecule energies passed to energy_lim f'xn
  min_energy = 0.0  # Minimum energy of the molecule
  max_energy = 0.0  # Maximum energy of the molecule

  line_seperation = 1.0   # Sets the amount of space between each of the molecule lines
  axis_offset = 0.25      # Offsets the positions from y = 0.

  def __init__(self, position, name, energy, surface):
    self.position = position
    self.name = name
    self.energy = energy
    self.surface = surface
    self.linecolor = 'black'
    self.linewidth = 5
    self.linethickness = 0.5
    self.x1, self.x2 = self.generate_xcoords(type(self).line_seperation, type(self).axis_offset, self.position, self.linethickness, type(self).molec_dict) 
    self.name_font_size = 10
    self.name_vert_scale = 0.04
    self.energy_font_size = 10
    self.energy_vert_scale = 0.04
    type(self).molec_dict[self.name] = self
    type(self).energy_list.append(float(self.energy))


  ##### First set of functions helps generate the molecules with default parameters ######

  @staticmethod
  def make_molecule(molecule_lines, molec_dict):
    """ Function creates objects in the molecule class. """

    for i in range(len(molecule_lines)):
      tmp = molecule_lines[i].strip().split()
      print(len(tmp))
      if len(tmp) == 3:
        molec_dict[tmp[0]] = Molecule((i+1), tmp[0], tmp[2], 0)
      elif len(tmp) == 5:
        ex_st_of = int(tmp[4])
        molec_dict[tmp[0]] = Molecule((i+1), tmp[0], tmp[2], ex_st_of)
        
    return None


  def generate_xcoords(self, line_seperation, axis_offset, position, linethickness, molec_dict):
    """ Computes the left and right endpoint x-coordinates of each molecule. """ 

    if self.surface == 0:
      x1 = (line_seperation * position) + axis_offset
      x2 = x1 + linethickness
    else:
      x1, x2 = self.generate_excited_coords(molec_dict)   

    return x1, x2

  def generate_excited_coords(self, molec_dict):
    """ Get excited coordinates. """

    for key, molecule in molec_dict.items():
      if molec_dict[key].position == self.surface:
        x1 = molec_dict[key].x1
        x2 = molec_dict[key].x2
    
    return x1, x2


  @staticmethod
  def energy_lim(energy_list):
    """ Obtain the minimum and maximum energy. """

    max_energy = max(energy_list)
    min_energy = min(energy_list)
    
    return max_energy, min_energy

  @staticmethod
  def get_count(energy_list):
    """ Figure out how many ground state and excited state molecules there are. """

    count = len(energy_list)

    return count

  #######################################################################################


  ### Change the default properties of each molecule according to user specifications ### 

  def get_name(self):
    return self.name
  
  @staticmethod
  def alter_molec_with_plot_specs(self, molecoptions_lines):
    """ User may specify changes to default molecules. 
        Input set-up:
        Molecule = (keyword1=val, keyword2=val, ...)     
  """

    # Need to parse the 

    for i in range(len(options_lines)):
      # Figure out the molecule object user wants to change
      species = options_lines.strip().split()[0]
      # Break out string to figure out what molecule attribute need to be changed and what new val is
      paren_string = options_lines[i][options_lines[i].find('(') + 1 : options_lines[i].find(')')]
      val_change_list = paren_string.split(',')
      for j in range(len(val_change_list)):
        prop = val_change_list[j].split('=')[0]
        new_val = val_change_list[j].split('=')[1]

    for key, value in molec_dict.items():      
      if  species == molec_dict[key].get_name(): 
        molec_dict[key].prop = new_val     

    return None


  def latexify_name(self,name):
      """ Convert the name into a format to make it in LaTEX style. """

      self.name = '$' + self.name + '$'

      return self.name

  #######################################################################################


  ##### Set of functions compute values needed for the plot using molecule properties  ##

  def calc_midpoint(self, x1, x2):
      """ Names of molecules are specified over the middle of the line. This function computes the midpoint for this. """

      midpoint = ( (x2 + x1) / 2 ) 

      return midpoint


  def vert_shift_name(self, min_energy, max_energy):
      """ Calculate how far below the molecule line the name will be shown. """

      name_position = float(self.energy) - self.name_vert_scale * (max_energy - min_energy)

      return name_position


  def vert_shift_energy(self, min_energy, max_energy):
      """ Calculate how far above the molecule line the energy will be shown. """

      energy_position = float(self.energy) + self.energy_vert_scale * (max_energy - min_energy) 

      return energy_position

  @classmethod
  def add_attributes_to_class(cls):
    """ Adds all the attributes to the class that could not be added upon initialization. """  

    cls.attribute = property(lambda cls: 'val of attribute')

    return None


  #######################################################################################

