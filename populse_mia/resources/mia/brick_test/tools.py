"""The smooth brick inherited from nipype/spm, just for unit testing purpose.

:Contains:
    :Class:
        - Smooth

"""

##########################################################################
# mia_processes - Copyright (C) IRMaGe/CEA, 2018
# Distributed under the terms of the CeCILL license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html
# for details.
##########################################################################

# Trait import
from traits.api import Float
from nipype.interfaces.base import (OutputMultiPath,
                                    InputMultiPath,
                                    File, traits)
from nipype.interfaces.spm.base import ImageFileSPM

from mia_processes.process_mia import Process_Mia

# Other import
import os
from nipype.interfaces import spm

class Smooth(Process_Mia):

    def __init__(self):
        super(Smooth, self).__init__()
        self.requirement = ['matlab', 'spm']

        # Inputs description
        in_files_desc = 'List of files to smooth. A list of items which are an existing, uncompressed file (valid extensions: [.img, .nii, .hdr]).'
        fwhm_desc = 'Full-width at half maximum (FWHM) of the Gaussian smoothing kernel in mm. A list of 3 items which are a float of fwhm for each dimension.'
        data_type_desc = 'Data type of the output images (an integer [int or long]).'
        implicit_masking_desc = 'A mask implied by a particular voxel value (a boolean).'
        out_prefix_desc = 'Specify  the string to be prepended to the filenames of the smoothed image file(s) (a string).'

        # Outputs description
        smoothed_files_desc = 'The smoothed files (a list of items which are an existing file name).'

        # Input traits
        self.add_trait("in_files",
                       InputMultiPath(ImageFileSPM(),
                                      copyfile=False,
                                      output=False,
                                      desc=in_files_desc))
        self.add_trait("fwhm",
                       traits.List([6, 6, 6],
                                   output=False,
                                   optional=True,
                                   desc= fwhm_desc))

        self.add_trait("data_type",
                       traits.Int(output=False,
                                  optional=True,
                       desc=data_type_desc))

        self.add_trait("implicit_masking",
                       traits.Bool(output=False,
                                   optional=True,
                                   desc=implicit_masking_desc))

        self.add_trait("out_prefix",
                       traits.String('s',
                                     usedefault=True,
                                     output=False,
                                     optional=True,
                                     desc=out_prefix_desc))

        # Output traits
        self.add_trait("smoothed_files",
                       OutputMultiPath(File(),
                                       output=True,
                                       desc=smoothed_files_desc))

        self.process = spm.Smooth()
        self.change_dir = True

    def list_outputs(self):
        super(Smooth, self).list_outputs()

        if self.outputs:
            self.outputs = {}

        if self.inheritance_dict:
            self.inheritance_dict = {}

        if self.in_files and self.in_files != [Undefined]:
            self.process.inputs.in_files = self.in_files

            if self.out_prefix:
                self.process.inputs.out_prefix = self.out_prefix

            self.outputs['smoothed_files'] = self.process._list_outputs()[
                                                               'smoothed_files']

        if self.outputs:
        
            for key, values in self.outputs.items():
            
                if key == "smoothed_files":
                
                    for fullname in values:
                        path, filename = os.path.split(fullname)
                    
                        if self.out_prefix:
                            filename_without_prefix = filename[
                                                          len(self.out_prefix):]
                        
                        else:
                            filename_without_prefix = filename[len('s'):]

                        if (os.path.join(path,
                                         filename_without_prefix)
                              in self.in_files):
                            self.inheritance_dict[fullname] = os.path.join(path,
                                                        filename_without_prefix)
        
        return self.make_initResult()

    def run_process_mia(self):
        super(Smooth, self).run_process_mia()

        for idx, element in enumerate(self.in_files):
            full_path = os.path.relpath(element)
            self.in_files[idx] = full_path

        self.process.inputs.in_files = self.in_files
        self.process.inputs.fwhm = self.fwhm
        self.process.inputs.data_type = self.data_type
        self.process.inputs.implicit_masking = self.implicit_masking
        self.process.inputs.out_prefix = self.out_prefix

        self.process.run()
