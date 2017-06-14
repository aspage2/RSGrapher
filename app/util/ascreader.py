## Class to read out ASC data from a file.
class ASCData:
    def __init__(self, filename):
        fh = open(filename)
        self.__skip_asc_header (fh)
        self.__x = []
        self.__y = []
        line = fh.readline().strip()
        while (line != ""):
            t, d, l = line.split("\t",2)
            self.__x.append (float(d))
            self.__y.append (float(l))
            line = fh.readline().strip()
        self.__xm = max(self.__x)
        self.__ym = max(self.__y)

    def __len__ (self):
        return len(self.__x)
    
    def disp_data (self):
        return tuple(self.__x)
    def load_data (self):
        return tuple(self.__y)
    
    def __getitem__ (self, i):
        return (self.__x[i], self.__y[i])
    def get_load (self, i):
        return self.__y[i]
    def get_disp (self, i):
        return self.__x[i]

    def get_max_load (self):
        return self.__ym
    def get_max_disp (self):
        return self.__xm
    
    def __skip_asc_header (self, fh):
        for i in range (7):
            fh.readline()