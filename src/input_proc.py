""" A repository of functions which process the information of the command line as well as the input file. """

import os
import sys
import argparse
from specs import Input
from specs import Molecule
from specs import PlotParameter
from specs import OutFileParameter


def input_processor():
    """ Checks command line input from user. Prints error messages if needed. Causes program to exit. """

    parser = argparse.ArgumentParser(description="Produces a plot of a computed potential energy surface.")

    parser.add_argument('-i', '--input', type=str, default='input.dat', help="Name of the input file to be read in")
    parser.add_argument('-o', '--output', type=str, default='output.dat', help="Name of the output file to be created.")

    args = parser.parse_args()

    Input.input_file_name = args.input
    Input.output_file_name = args.output

    if not os.path.exists(Input.input_file_name):
        print("Could not locate input file: " + Input.input_file_name)
        sys.exit()

    return None


def section_finder():
    """ Checks for section headers and calls appropriate function if the finder is found. """

    with open(Input.input_file_name, 'r') as infile:
        Input.input_file_content = infile.readlines()

    Input.input_file_length = len(Input.input_file_content)

    for i in range(0, Input.input_file_length):
        if '$energies' in Input.input_file_content[i]:
            energy_processor(i)
        if '$connect' in Input.input_file_content[i]:
            connection_processor(i)
        if '$images' in Input.input_file_content[i]:
            image_processor(i)
        if '$plot_format' in Input.input_file_content[i]:
            plot_format_processor(i)
        if '$output_file' in Input.input_file_content[i]:
            output_file_processor(i)

    calc_stuff()

    return None


def energy_processor(section_start):
    """ Reads the information for each molecular species that the user is interested in. """

    for i in range(section_start + 1, Input.input_file_length):
        tmp = Input.input_file_content[i].lstrip().rstrip().split()
        if '#' not in tmp[0]:
            if '$end' in tmp[0]:
                break
            elif 'excite' not in tmp:
                Molecule.species_count += 1
                Molecule.ground_species_count += 1
                Molecule.number.append(int(tmp[0]))
                Molecule.name.append(str(tmp[2]))
                Molecule.energy.append(float(tmp[4]))
            else:
                Molecule.species_count += 1
                Molecule.excited_species_count += 1
                Molecule.number.append(int(tmp[0]))
                Molecule.name.append(str(tmp[2]))
                Molecule.energy.append(float(tmp[4]))
                Molecule.excited_state.append(int(tmp[8]))
                Molecule.excited_surface.append(int(tmp[10]))

    Molecule.range_energy = max(Molecule.energy) - min(Molecule.energy)
    Molecule.max_energy = max(Molecule.energy)
    Molecule.min_energy = min(Molecule.energy)

    return None


def connection_processor(section_start):
    """ Processes information to plot out the connection lines. """

    Molecule.connection_type = Input.input_file_content[section_start + 1].lstrip().rstrip().lower()

    for i in range(section_start + 2, Input.input_file_length):
        tmp = Input.input_file_content[i].lstrip().rstrip().split()
        if '#' not in tmp[0]:
            if '$end' in tmp[0]:
                break
            else:
                if Molecule.connection_type == 'numbers':
                    Molecule.connection_count += 1
                    Molecule.left_connection.append(int(tmp[0]))
                    Molecule.right_connection.append(int(tmp[2]))
                elif Molecule.connection_type == 'names':
                    Molecule.connection_count += 1
                    # if check_excite == -1: Need an excited check to know to change loops for xcited plotting
                    for k in range(0, Molecule.species_count):
                        if Molecule.name[k] == tmp[0]:
                            Molecule.left_connection.append(int(Molecule.number[k]))
                        if Molecule.name[k] == tmp[2]:
                            Molecule.right_connection.append(int(Molecule.number[k]))
                else:
                    print('Connect section formatted improperly.')
                    sys.exit()

    return None


def image_processor(section_start):
    """ Processes information to plot out images. """

    for i in range(section_start + 1, Input.input_file_length):
        tmp = Input.input_file_content[i].lstrip().rstrip().split()
        if '#' not in tmp[0]:
            if '$end' in tmp[0]:
                break
            else:
                # check_image = 0
                Molecule.image_number.append(int(tmp[0]))
                Molecule.image_name.append(str(tmp[2]))

    return None


def plot_format_processor(section_start):
    """ Processes information to format the plot. """

    for i in range(section_start + 1, Input.input_file_length):
        tmp = Input.input_file_content[i].lstrip().rstrip().split()
        if '#' not in tmp[0]:
            if '$end' in tmp[0]:
                break
            else:
                if 'y_axis_top_extend' in tmp[0]:
                    PlotParameter.y_axis_top_extend = float(tmp[2])
                if 'y_axis_bot_extend' in tmp[0]:
                    PlotParameter.y_axis_bot_extend = float(tmp[2])
                if 'y_axis_label' in tmp[0]:
                    PlotParameter.y_axis_label = str(tmp[2])
                if 'x_axis_right_extend' in tmp[0]:
                    PlotParameter.x_axis_right_extend = float(tmp[2])
                if 'x_axis_label' in tmp[0]:
                    PlotParameter.x_axis_label = str(tmp[2])
                if 'name_vshift_scale' in tmp[0]:
                    PlotParameter.scale_fact_name_vshift = float(tmp[2])
                if 'name_font_size' in tmp[0]:
                    PlotParameter.name_font_size = int(tmp[2])
                if 'energy_vshift_scale' in tmp[0]:
                    PlotParameter.scale_fact_energy_vshift = float(tmp[2])
                if 'energy_font_size' in tmp[0]:
                    PlotParameter.energy_font_size = int(tmp[2])
                if 'species_line_spacing' in tmp[0]:
                    PlotParameter.species_line_spacing = float(tmp[2])
                if 'species_line_length' in tmp[0]:
                    PlotParameter.species_line_length = float(tmp[2])
                if 'species_line_width' in tmp[0]:
                    PlotParameter.species_line_width = float(tmp[2])
                if 'connection_line_width' in tmp[0]:
                    PlotParameter.connection_line_width = float(tmp[2])
                if 'latex_text = on' in tmp[0]:
                    PlotParameter.name_latex_format = 'on'
                    # else:
                    # print("improper formatting of plot section")

    return None


def output_file__processor():
    """ Processes information that formats the input file. """

    for i in range(section_start + 1, Input.input_file_length):
        tmp = Input.input_file_content[i].lstrip().rstrip().split()
        if '#' not in tmp[0]:
            if '$end' in tmp[0]:
                break
            else:
                if 'type' in tmp[0]:
                    OutFileParameter.type = int(tmp[2])
                if 'name' in tmp[0]:
                    OutFileParameter.name = str(tmp[2])
                if 'width' in tmp[0]:
                    OutFileParameter.width = int(tmp[2])
                if 'height' in tmp[0]:
                    OutFileParameter.length = int(tmp[2])
                if 'dpi' in tmp[0]:
                    OutFileParameter.dpi = int(tmp[2])

    return None


def calc_stuff():
    """ Using input from user, determine parameters for plot formatting. """

    PlotParameter.name_vshift = PlotParameter.name_vshift_scale_fact * Molecule.range_energy
    PlotParameter.energy_vshift = PlotParameter.energy_vshift_scale_fact * Molecule.range_energy
    PlotParameter.y_axis_top_lim = Molecule.max_energy + PlotParameter.y_axis_top_extend
    PlotParameter.y_axis_bot_lim = Molecule.min_energy - PlotParameter.y_axis_bot_extend
    PlotParameter.x_axis_right_lim = Molecule.ground_species_count + PlotParameter.x_axis_right_extend

    if PlotParameter.name_latex_format == 'on':
        for k in range(0, Molecule.species_count):
            tmp = '$' + name[k] + '$'
            name[k] = tmp
