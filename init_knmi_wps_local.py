from knmi_wps_processes import *
from knmi_wps_processes import wps_knmi
from knmi_wps_processes import wps_knmi_processes
from knmi_wps_processes.wps_knmi import KnmiWpsProcess
from pywps.Process import Status, WPSProcess

#
# run from run.wps.here.py (this allows the local cgi to be used...)
# author: ANDREJ
# tests provenance with knmi wps.
#



# target this function with __init__.py from the wps.py process.

#Override status class and method in order to print to stdout directly.
class MyStatus(Status):
    def set(self,string1,p):
        print string1 
status = MyStatus()

### Basic Example applies to most ..
# #
# http://pc150396.knmi.nl:9080/impactportal/WPS?
#   service=WPS&request=execute&identifier=wps_andrej&version=1.0.0&storeexecuteresponse=true
# 
class AndrejWpsProcess(WPSProcess):

    def __init__(self):
        WPSProcess.__init__(self, 
                            identifier = 'wps_andrej', # only mandatary attribute = same file name
                            title = 'Andrej tests wps',
                            abstract = 'WPS without lineage',
                            version = "1.0",
                            storeSupported = 'true',
                            statusSupported = 'true',
                            grassLocation =False)

    def execute(self):
        print "ANDREJ!ANDREJ!ANDREJ!"

        self.status.set("ready",100);

# knmi_process = wps_knmi.KnmiWpsProcess()
# knmi_process.status = status
# knmi_process.execute()

# class Generic(wps_knmi.KnmiWpsProcess):
#     # KnmiWebProcessDescriptor
#     def __init__(self):
#         wps_knmi.KnmiWpsProcess.__init__(self , wps_knmi.KnmiWebProcessDescriptor() )

# class Validate(wps_knmi.KnmiWpsProcess):
#     # KnmiWebProcessDescriptor
#     def __init__(self):
#         wps_knmi.KnmiWpsProcess.__init__(self , wps_knmi.KnmiClipcValidationDescriptor() )
       
class Copy(KnmiWpsProcess):
    # KnmiWebProcessDescriptor
    def __init__(self):
        KnmiWpsProcess.__init__(self , wps_knmi_processes.KnmiCopyDescriptor())

class Weight(KnmiWpsProcess):
    # KnmiWebProcessDescriptor
    def __init__(self):
        KnmiWpsProcess.__init__(self , wps_knmi_processes.KnmiWeightCopyDescriptor())

class Combine(KnmiWpsProcess):
    # KnmiWebProcessDescriptor
    def __init__(self):
        KnmiWpsProcess.__init__(self , wps_knmi_processes.KnmiCombineDescriptor())



knmiprocess = Weight()

knmiprocess.inputs['netcdf_source'].setValue( {'value':'http://opendap.knmi.nl/knmi/thredds/dodsC/CLIPC/cerfacs/vDTR/MPI-M-MPI-ESM-LR_rcp85_r1i1p1_SMHI-RCA4_v1/vDTR_JAN_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_SMHI-RCA4_v1_EUR-11_2006-2100.nc'})
knmiprocess.inputs['netcdf_target'].setValue( {'value':'COPY_NORM1.nc'} )
knmiprocess.inputs['weight'].setValue( {'value' : 'normminmax' } )
knmiprocess.inputs['variable'].setValue( {'value' : 'vDTR' } )
knmiprocess.inputs['tags'].setValue( {'value' : 'ale' } )

knmiprocess.status = status
knmiprocess.execute()

knmiprocess.inputs['netcdf_source'].setValue( {'value':'COPY_NORM1.nc'})
knmiprocess.inputs['netcdf_target'].setValue( {'value':'COPY_JAN.nc'} )
knmiprocess.inputs['weight'].setValue( {'value' : '0.5' } )
knmiprocess.inputs['variable'].setValue( {'value' : 'vDTR' } )
knmiprocess.inputs['tags'].setValue( {'value' : 'ale' } )

knmiprocess.status = status
knmiprocess.execute()

knmiprocess.inputs['netcdf_source'].setValue( {'value':'http://opendap.knmi.nl/knmi/thredds/dodsC/CLIPC/cerfacs/vDTR/MPI-M-MPI-ESM-LR_rcp85_r1i1p1_SMHI-RCA4_v1/vDTR_JUL_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_SMHI-RCA4_v1_EUR-11_2006-2100.nc'})
knmiprocess.inputs['netcdf_target'].setValue( {'value':'COPY_NORM2.nc'} )
knmiprocess.inputs['weight'].setValue(   {'value' : 'normstndrd' } )
knmiprocess.inputs['variable'].setValue( {'value' : 'vDTR' } )
knmiprocess.inputs['tags'].setValue( {'value' : 'ale' } )

knmiprocess.status = status
knmiprocess.execute()

knmiprocess.inputs['netcdf_source'].setValue( {'value':'COPY_NORM2.nc'})
knmiprocess.inputs['netcdf_target'].setValue( {'value':'COPY_JUL.nc'} )
knmiprocess.inputs['weight'].setValue( {'value' : '0.5' } )
knmiprocess.inputs['variable'].setValue( {'value' : 'vDTR' } )
knmiprocess.inputs['tags'].setValue( {'value' : 'ale' } )

knmiprocess.status = status
knmiprocess.execute()

knmiprocess = Combine()
knmiprocess.inputs['netcdf_source1'].setValue( {'value':'COPY_JAN.nc'})
knmiprocess.inputs['netcdf_source2'].setValue( {'value':'COPY_JUL.nc'})

knmiprocess.inputs['variable1'].setValue( {'value' : 'vDTR' } )
knmiprocess.inputs['variable2'].setValue( {'value' : 'vDTR' } )

knmiprocess.inputs['netcdf_target'].setValue( {'value':'COPY_COMBINE_YEAR.nc'})

knmiprocess.inputs['operation'].setValue( {'value' : 'subtract' } )
knmiprocess.inputs['tags'].setValue( {'value' : 'ale' } )

knmiprocess.status = status
knmiprocess.execute()

