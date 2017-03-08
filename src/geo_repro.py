from osgeo import osr,ogr
import sys,csv

class Transform(object):
    def __init__(self,s_srs,t_srs,in_csv,out_csv,delimiter=',',quotechar='|'):
        self.s_srs = osr.SpatialReference()
        self.t_srs = osr.SpatialReference()
        self.s_srs.ImportFromEPSG(s_srs)
        self.t_srs.ImportFromEPSG(t_srs)
        infile = open(in_csv, 'rb')
        outfile = open(out_csv, 'wb')
        csvreader = csv.reader(infile, delimiter=delimiter, quotechar=quotechar)
        csvwriter = csv.writer(outfile, delimiter=delimiter, quotechar=quotechar)
        for row in csvreader:
            inx,iny=[float(coord) for coord in row]
            csvwriter.writerow(self.transform(inx,iny))

        del csvreader
        del csvwriter
        infile.close()
        outfile.close()

    def transform(self,xcoord,ycoord):
        geom = ogr.Geometry(ogr.wkbPoint)
        geom.SetPoint_2D(0, xcoord,ycoord)
        geom.AssignSpatialReference(self.s_srs)
        geom.TransformTo(self.t_srs)
        return geom.GetPoint_2D()

if __name__=='__main__':
    #testing
    s_srs=26986
    t_srs=4326
    #in_csv='in_file.csv'
    #out_csv='out_file.csv'

    s_srs=int(sys.argv[1])
    t_srs=int(sys.argv[2])