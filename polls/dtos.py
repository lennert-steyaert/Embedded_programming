
#################################################################
#///////////////////////////////////////////////////////////////#
#################################################################
#               This file contains all DTO's
#################################################################
#///////////////////////////////////////////////////////////////#
#################################################################

##################################################
#              DTO for device object
##################################################

class DTODevice:
    pk = 0
    IO = []
    device = None

##################################################
#              DTO for IO object
##################################################

class DTOIO:
    pk = 0
    device = 0
    IO = None
     
