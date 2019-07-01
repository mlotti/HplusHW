
#tau n.o. 2 can be 0 and 0 w[]hen it is not anti-isoated

tauPt_1 = [0,1,2]
decayMode_1 = [0,1,2]
tauPt_2 = [-1,0,1,2]
decayMode_2 = [-1,0,1,2]


#1 prong + zero pi

FR_1 = [0.25,0.20,0.20]

#1 prong + 1 pi

FR_2 = [0.25,0.21,0.19]

#3 prong + zero pi

FR_3 = [0.16,0.17,0.17]

a = -99

w = []

# one anti-iso: 1FR/(1-1FR)
# tw[]o anti-iso: 1FR*2FR/((1-1FR)*(1-2FR))


for de2 in decayMode_2:

  for pt2 in tauPt_2:

    for de1 in decayMode_1:

      for pt1 in tauPt_1:

        if (pt2==-1 or de2 == -1):
          if (de1 == 0):
            a= FR_1[pt1]/(1-FR_1[pt1])

          if (de1 == 1):
            a= FR_2[pt1]/(1-FR_2[pt1])

          if (de1 == 2):
            a= FR_3[pt1]/(1-FR_3[pt1])

        else:
          if (de1 == 0 and de2 ==0):
            a= FR_1[pt1]*FR_1[pt2]/((1-FR_1[pt1])*(1-FR_1[pt2]))

          if (de1 == 1 and de2 ==0):
            a= FR_2[pt1]*FR_1[pt2]/((1-FR_2[pt1])*(1-FR_1[pt2]))

          if (de1 == 2 and de2 ==0):
            a= FR_3[pt1]*FR_1[pt2]/((1-FR_3[pt1])*(1-FR_1[pt2]))

          if (de1 == 0 and de2 ==1):
            a= FR_1[pt1]*FR_2[pt2]/((1-FR_1[pt1])*(1-FR_2[pt2]))

          if (de1 == 1 and de2 ==1):
            a= FR_2[pt1]*FR_2[pt2]/((1-FR_2[pt1])*(1-FR_2[pt2]))

          if (de1 == 2 and de2 ==1):
            a= FR_3[pt1]*FR_2[pt2]/((1-FR_3[pt1])*(1-FR_2[pt2]))

          if (de1 == 0 and de2 ==2):
            a= FR_1[pt1]*FR_3[pt2]/((1-FR_1[pt1])*(1-FR_3[pt2]))

          if (de1 == 1 and de2 ==2):
            a= FR_2[pt1]*FR_3[pt2]/((1-FR_2[pt1])*(1-FR_3[pt2]))

          if (de1 == 2 and de2 ==2):
            a= FR_3[pt1]*FR_3[pt2]/((1-FR_3[pt1])*(1-FR_3[pt2]))

#        print w[]
        w.append(a)



print "  'tauPt_1lt40:decayMode_1lt2:tauPt_2lt20:decayMode_2lt1'   :", w[0] , ","
print "  'tauPt_1eq40to60:decayMode_1lt2:tauPt_2lt20:decayMode_2lt1'   :", w[1] , ","
print "  'tauPt_1gt60:decayMode_1lt2:tauPt_2lt20:decayMode_2lt1'   :", w[2] , ","
print "  'tauPt_1lt40:decayMode_1eq2to3:tauPt_2lt20:decayMode_2lt1'   :", w[3] , ","
print "  'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2lt1'   :", w[4] , ","
print "  'tauPt_1gt60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2lt1'   :", w[5] , ","
print "  'tauPt_1lt40:decayMode_1gt3:tauPt_2lt20:decayMode_2lt1'   :", w[6] , ","
print "  'tauPt_1eq40to60:decayMode_1gt3:tauPt_2lt20:decayMode_2lt1'   :", w[7] , ","
print "  'tauPt_1gt60:decayMode_1gt3:tauPt_2lt20:decayMode_2lt1'   :", w[8] , ","
print "  'tauPt_1lt40:decayMode_1lt2:tauPt_2eq20to40:decayMode_2lt1'   :", w[9] , ","
print "  'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2lt1'   :", w[10] , ","
print "  'tauPt_1gt60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2lt1'   :", w[11] , ","
print "  'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2lt1'   :", w[12] , ","
print "  'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2lt1'   :", w[13] , ","
print "  'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2lt1'   :", w[14] , ","
print "  'tauPt_1lt40:decayMode_1gt3:tauPt_2eq20to40:decayMode_2lt1'   :", w[15] , ","
print "  'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2lt1'   :", w[16] , ","
print "  'tauPt_1gt60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2lt1'   :", w[17] , ","
print "  'tauPt_1lt40:decayMode_1lt2:tauPt_2eq40to60:decayMode_2lt1'   :", w[18] , ","
print "  'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2lt1'   :", w[19] , ","
print "  'tauPt_1gt60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2lt1'   :", w[20] , ","
print "  'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2lt1'   :", w[21] , ","
print "  'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2lt1'   :", w[22] , ","
print "  'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2lt1'   :", w[23] , ","
print "  'tauPt_1lt40:decayMode_1gt3:tauPt_2eq40to60:decayMode_2lt1'   :", w[24] , ","
print "  'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2lt1'   :", w[25] , ","
print "  'tauPt_1gt60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2lt1'   :", w[26] , ","
print "  'tauPt_1lt40:decayMode_1lt2:tauPt_2gt60:decayMode_2lt1'   :", w[27] , ","
print "  'tauPt_1eq40to60:decayMode_1lt2:tauPt_2gt60:decayMode_2lt1'   :", w[28] , ","
print "  'tauPt_1gt60:decayMode_1lt2:tauPt_2gt60:decayMode_2lt1'   :", w[29] , ","
print "  'tauPt_1lt40:decayMode_1eq2to3:tauPt_2gt60:decayMode_2lt1'   :", w[30] , ","
print "  'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2lt1'   :", w[31] , ","
print "  'tauPt_1gt60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2lt1'   :", w[32] , ","
print "  'tauPt_1lt40:decayMode_1gt3:tauPt_2gt60:decayMode_2lt1'   :", w[33] , ","
print "  'tauPt_1eq40to60:decayMode_1gt3:tauPt_2gt60:decayMode_2lt1'   :", w[34] , ","
print "  'tauPt_1gt60:decayMode_1gt3:tauPt_2gt60:decayMode_2lt1'   :", w[35] , ","
print "  'tauPt_1lt40:decayMode_1lt2:tauPt_2lt20:decayMode_2eq1to2'   :", w[36] , ","
print "  'tauPt_1eq40to60:decayMode_1lt2:tauPt_2lt20:decayMode_2eq1to2'   :", w[37] , ","
print "  'tauPt_1gt60:decayMode_1lt2:tauPt_2lt20:decayMode_2eq1to2'   :", w[38] , ","
print "  'tauPt_1lt40:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq1to2'   :", w[39] , ","
print "  'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq1to2'   :", w[40] , ","
print "  'tauPt_1gt60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq1to2'   :", w[41] , ","
print "  'tauPt_1lt40:decayMode_1gt3:tauPt_2lt20:decayMode_2eq1to2'   :", w[42] , ","
print "  'tauPt_1eq40to60:decayMode_1gt3:tauPt_2lt20:decayMode_2eq1to2'   :", w[43] , ","
print "  'tauPt_1gt60:decayMode_1gt3:tauPt_2lt20:decayMode_2eq1to2'   :", w[44] , ","
print "  'tauPt_1lt40:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq1to2'   :", w[45] , ","
print "  'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq1to2'   :", w[46] , ","
print "  'tauPt_1gt60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq1to2'   :", w[47] , ","
print "  'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq1to2'   :", w[48] , ","
print "  'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq1to2'   :", w[49] , ","
print "  'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq1to2'   :", w[50] , ","
print "  'tauPt_1lt40:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq1to2'   :", w[51] , ","
print "  'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq1to2'   :", w[52] , ","
print "  'tauPt_1gt60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq1to2'   :", w[53] , ","
print "  'tauPt_1lt40:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq1to2'   :", w[54] , ","
print "  'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq1to2'   :", w[55] , ","
print "  'tauPt_1gt60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq1to2'   :", w[56] , ","
print "  'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq1to2'   :", w[57] , ","
print "  'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq1to2'   :", w[58] , ","
print "  'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq1to2'   :", w[59] , ","
print "  'tauPt_1lt40:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq1to2'   :", w[60] , ","
print "  'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq1to2'   :", w[61] , ","
print "  'tauPt_1gt60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq1to2'   :", w[62] , ","
print "  'tauPt_1lt40:decayMode_1lt2:tauPt_2gt60:decayMode_2eq1to2'   :", w[63] , ","
print "  'tauPt_1eq40to60:decayMode_1lt2:tauPt_2gt60:decayMode_2eq1to2'   :", w[64] , ","
print "  'tauPt_1gt60:decayMode_1lt2:tauPt_2gt60:decayMode_2eq1to2'   :", w[65] , ","
print "  'tauPt_1lt40:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq1to2'   :", w[66] , ","
print "  'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq1to2'   :", w[67] , ","
print "  'tauPt_1gt60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq1to2'   :", w[68] , ","
print "  'tauPt_1lt40:decayMode_1gt3:tauPt_2gt60:decayMode_2eq1to2'   :", w[69] , ","
print "  'tauPt_1eq40to60:decayMode_1gt3:tauPt_2gt60:decayMode_2eq1to2'   :", w[70] , ","
print "  'tauPt_1gt60:decayMode_1gt3:tauPt_2gt60:decayMode_2eq1to2'   :", w[71] , ","
print "  'tauPt_1lt40:decayMode_1lt2:tauPt_2lt20:decayMode_2eq2to3'   :", w[72] , ","
print "  'tauPt_1eq40to60:decayMode_1lt2:tauPt_2lt20:decayMode_2eq2to3'   :", w[73] , ","
print "  'tauPt_1gt60:decayMode_1lt2:tauPt_2lt20:decayMode_2eq2to3'   :", w[74] , ","
print "  'tauPt_1lt40:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq2to3'   :", w[75] , ","
print "  'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq2to3'   :", w[76] , ","
print "  'tauPt_1gt60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq2to3'   :", w[77] , ","
print "  'tauPt_1lt40:decayMode_1gt3:tauPt_2lt20:decayMode_2eq2to3'   :", w[78] , ","
print "  'tauPt_1eq40to60:decayMode_1gt3:tauPt_2lt20:decayMode_2eq2to3'   :", w[79] , ","
print "  'tauPt_1gt60:decayMode_1gt3:tauPt_2lt20:decayMode_2eq2to3'   :", w[80] , ","
print "  'tauPt_1lt40:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq2to3'   :", w[81] , ","
print "  'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq2to3'   :", w[82] , ","
print "  'tauPt_1gt60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq2to3'   :", w[83] , ","
print "  'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq2to3'   :", w[84] , ","
print "  'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq2to3'   :", w[85] , ","
print "  'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq2to3'   :", w[86] , ","
print "  'tauPt_1lt40:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq2to3'   :", w[87] , ","
print "  'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq2to3'   :", w[88] , ","
print "  'tauPt_1gt60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq2to3'   :", w[89] , ","
print "  'tauPt_1lt40:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq2to3'   :", w[90] , ","
print "  'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq2to3'   :", w[91] , ","
print "  'tauPt_1gt60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq2to3'   :", w[92] , ","
print "  'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq2to3'   :", w[93] , ","
print "  'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq2to3'   :", w[94] , ","
print "  'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq2to3'   :", w[95] , ","
print "  'tauPt_1lt40:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq2to3'   :", w[96] , ","
print "  'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq2to3'   :", w[97] , ","
print "  'tauPt_1gt60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq2to3'   :", w[98] , ","
print "  'tauPt_1lt40:decayMode_1lt2:tauPt_2gt60:decayMode_2eq2to3'   :", w[99] , ","
print "  'tauPt_1eq40to60:decayMode_1lt2:tauPt_2gt60:decayMode_2eq2to3'   :", w[100] , ","
print "  'tauPt_1gt60:decayMode_1lt2:tauPt_2gt60:decayMode_2eq2to3'   :", w[101] , ","
print "  'tauPt_1lt40:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq2to3'   :", w[102] , ","
print "  'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq2to3'   :", w[103] , ","
print "  'tauPt_1gt60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq2to3'   :", w[104] , ","
print "  'tauPt_1lt40:decayMode_1gt3:tauPt_2gt60:decayMode_2eq2to3'   :", w[105] , ","
print "  'tauPt_1eq40to60:decayMode_1gt3:tauPt_2gt60:decayMode_2eq2to3'   :", w[106] , ","
print "  'tauPt_1gt60:decayMode_1gt3:tauPt_2gt60:decayMode_2eq2to3'   :", w[107] , ","
print "  'tauPt_1lt40:decayMode_1lt2:tauPt_2lt20:decayMode_2gt3'   :", w[108] , ","
print "  'tauPt_1eq40to60:decayMode_1lt2:tauPt_2lt20:decayMode_2gt3'   :", w[109] , ","
print "  'tauPt_1gt60:decayMode_1lt2:tauPt_2lt20:decayMode_2gt3'   :", w[110] , ","
print "  'tauPt_1lt40:decayMode_1eq2to3:tauPt_2lt20:decayMode_2gt3'   :", w[111] , ","
print "  'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2gt3'   :", w[112] , ","
print "  'tauPt_1gt60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2gt3'   :", w[113] , ","
print "  'tauPt_1lt40:decayMode_1gt3:tauPt_2lt20:decayMode_2gt3'   :", w[114] , ","
print "  'tauPt_1eq40to60:decayMode_1gt3:tauPt_2lt20:decayMode_2gt3'   :", w[115] , ","
print "  'tauPt_1gt60:decayMode_1gt3:tauPt_2lt20:decayMode_2gt3'   :", w[116] , ","
print "  'tauPt_1lt40:decayMode_1lt2:tauPt_2eq20to40:decayMode_2gt3'   :", w[117] , ","
print "  'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2gt3'   :", w[118] , ","
print "  'tauPt_1gt60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2gt3'   :", w[119] , ","
print "  'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2gt3'   :", w[120] , ","
print "  'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2gt3'   :", w[121] , ","
print "  'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2gt3'   :", w[122] , ","
print "  'tauPt_1lt40:decayMode_1gt3:tauPt_2eq20to40:decayMode_2gt3'   :", w[123] , ","
print "  'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2gt3'   :", w[124] , ","
print "  'tauPt_1gt60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2gt3'   :", w[125] , ","
print "  'tauPt_1lt40:decayMode_1lt2:tauPt_2eq40to60:decayMode_2gt3'   :", w[126] , ","
print "  'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2gt3'   :", w[127] , ","
print "  'tauPt_1gt60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2gt3'   :", w[128] , ","
print "  'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2gt3'   :", w[129] , ","
print "  'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2gt3'   :", w[130] , ","
print "  'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2gt3'   :", w[131] , ","
print "  'tauPt_1lt40:decayMode_1gt3:tauPt_2eq40to60:decayMode_2gt3'   :", w[132] , ","
print "  'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2gt3'   :", w[133] , ","
print "  'tauPt_1gt60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2gt3'   :", w[134] , ","
print "  'tauPt_1lt40:decayMode_1lt2:tauPt_2gt60:decayMode_2gt3'   :", w[135] , ","
print "  'tauPt_1eq40to60:decayMode_1lt2:tauPt_2gt60:decayMode_2gt3'   :", w[136] , ","
print "  'tauPt_1gt60:decayMode_1lt2:tauPt_2gt60:decayMode_2gt3'   :", w[137] , ","
print "  'tauPt_1lt40:decayMode_1eq2to3:tauPt_2gt60:decayMode_2gt3'   :", w[138] , ","
print "  'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2gt3'   :", w[139] , ","
print "  'tauPt_1gt60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2gt3'   :", w[140] , ","
print "  'tauPt_1lt40:decayMode_1gt3:tauPt_2gt60:decayMode_2gt3'   :", w[141] , ","
print "  'tauPt_1eq40to60:decayMode_1gt3:tauPt_2gt60:decayMode_2gt3'   :", w[142] , ","
print "  'tauPt_1gt60:decayMode_1gt3:tauPt_2gt60:decayMode_2gt3'   :", w[143] , ","

