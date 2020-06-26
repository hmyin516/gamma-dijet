from ROOT import *
import numpy as np

doreweight = 0
inputvar = "bdt"
mc = "sherpa_SF"
var = inputvar
ntrackall = TFile("ROOT/dijet_sherpa_py_forGamma.root")
ntrackall3  = TFile("ROOT/dijet_data_py_forGamma.root")
gammasherpa = TFile("ROOT/gammajet_sherpa.root")
gammadata = TFile("ROOT/gammajet_data.root")

def myText(x,y,text,color =1):
    l = TLatex()
    l.SetTextSize(0.025)
    l.SetNDC()
    l.SetTextColor(color)
    l.DrawLatex(x,y,text)
    pass

bin = [0,50,100,150,200,300,400,500,600,800,1000,1200,1500,2000]
for i in range(0,8):   #for only dijet event, start from jet pT>500 GeV
#for i in range(13):	#for gamma+jet combined with dijet event, start from jet pT>0 GeV
    min = bin[i]
    max = bin[i+1]

    #input variables
    # sim
    dijet_quark = ntrackall.Get(str(min)+"_LeadingJet_Forward_Quark_"+inputvar)
    dijet_subjetquark = ntrackall.Get(str(min)+"_SubJet_Forward_Quark_"+inputvar)

    dijet_gluon = ntrackall.Get(str(min)+"_LeadingJet_Forward_Gluon_"+inputvar)
    dijet_subjetgluon = ntrackall.Get(str(min)+"_SubJet_Forward_Gluon_"+inputvar)

    dijet_quark2 = ntrackall.Get(str(min)+"_LeadingJet_Central_Quark_"+inputvar)
    dijet_subjetquark2 = ntrackall.Get(str(min)+"_SubJet_Central_Quark_"+inputvar)

    dijet_gluon2 = ntrackall.Get(str(min)+"_LeadingJet_Central_Gluon_"+inputvar)
    dijet_subjetgluon2 = ntrackall.Get(str(min)+"_SubJet_Central_Gluon_"+inputvar)

    gamma_quark = gammasherpa.Get(str(min) + "_LeadingJet_Central_Quark_" + inputvar)
    gamma_gluon = gammasherpa.Get(str(min) + "_LeadingJet_Central_Gluon_" + inputvar)

    # data 
    dijet_data1 = ntrackall3.Get(str(min)+"_LeadingJet_Forward_Data_"+inputvar)
    dijet_data2 = ntrackall3.Get(str(min)+"_LeadingJet_Central_Data_"+inputvar)
    dijet_data3 = ntrackall3.Get(str(min)+"_SubJet_Forward_Data_" + inputvar)
    dijet_data4 = ntrackall3.Get(str(min)+"_SubJet_Central_Data_" + inputvar)

    gamma_data = gammadata.Get(str(min)+"_LeadingJet_Central_Data_"+inputvar)


    #adding data together
    dijet_data1.Add(dijet_data2)
    dijet_data3.Add(dijet_data4)
   
    # checking for nan bins in dijet sample (quick fix) 
    def checkNan(jet1,jet2,numRange):
        for a in range(numRange):
		    if np.isnan(jet1.GetBinContent(a)):
			    jet1.SetBinContent(a,0)
		    if np.isnan(jet2.GetBinContent(a)):
			    jet2.SetBinContent(a,0)
 
    checkNan(dijet_quark,dijet_quark2,60)
    checkNan(dijet_gluon,dijet_gluon2,60)
    checkNan(dijet_subjetquark,dijet_subjetquark2,60)
    checkNan(dijet_subjetgluon,dijet_subjetgluon2,60)
    
    #adding dijet and subjet together
    dijet_quark.Add(dijet_quark2)
    dijet_gluon.Add(dijet_gluon2)
    dijet_subjetquark.Add(dijet_subjetquark2)
    dijet_subjetgluon.Add(dijet_subjetgluon2)
    dijet_quark.Add(dijet_subjetquark)
    dijet_gluon.Add(dijet_subjetgluon)
    dijet_data1.Add(dijet_data3)
    
    #reassigning to variables for convienece
    higher_quark = gamma_quark
    higher_gluon = gamma_gluon
    lower_quark = dijet_quark
    lower_gluon = dijet_gluon
    higher_data = gamma_data
    lower_data = dijet_data1

    #add leading and subleading jet from only dijet event together,
    #note that for gammajet+dijet event, we need to add leading jet from gammajet and leading jet from dijet sample together
    ToT_Fq2 = 0.
    ToT_Fg2 = 0.
    ToT_Cq2 =0.
    ToT_Cg2 = 0.

    for j in range(1,lower_quark.GetNbinsX()+1):
		ToT_Fq2+=higher_quark.GetBinContent(j)  #dijetquark
		ToT_Cq2+=lower_quark.GetBinContent(j) #gammaquark
		ToT_Fg2+=higher_gluon.GetBinContent(j) #dijetgluon
		ToT_Cg2+=lower_gluon.GetBinContent(j)#gammagluon

    # calculate the fraction of each sample 
    if ((ToT_Fg2+ToT_Fq2) != 0):
		fg=ToT_Fg2/(ToT_Fg2+ToT_Fq2)
		cg=ToT_Cg2/(ToT_Cq2+ToT_Cg2)
    else:
		continue
    fq=1.-fg
    cq=1.-cg

    c = TCanvas("c","c",500,500)
    if (doreweight):
        for i in range(1,higher_quark.GetNbinsX()+1):
            if (lower_quark.GetBinContent(i) > 0 and lower_gluon.GetBinContent(i) > 0):
                
                factor_gluon = higher_gluon.GetBinContent(i)/lower_gluon.GetBinContent(i)
                factor_quark = higher_quark.GetBinContent(i)/lower_quark.GetBinContent(i)
                lower_quark.SetBinContent(i,lower_quark.GetBinContent(i)*factor_quark)
                lower_gluon.SetBinContent(i,lower_gluon.GetBinContent(i)*factor_quark)
                lower_data.SetBinContent(i,lower_data.GetBinContent(i)*factor_quark)
                pass
            pass
        pass

    if (lower_quark.Integral() != 0):
        lower_quark.Scale(1./lower_quark.Integral())
    if(lower_gluon.Integral() != 0):
        lower_gluon.Scale(1./lower_gluon.Integral())
    if(higher_quark.Integral() != 0):
        higher_quark.Scale(1./higher_quark.Integral())
    if(higher_gluon.Integral() != 0):
        higher_gluon.Scale(1./higher_gluon.Integral())
    if(lower_data.Integral() != 0):
        lower_data.Scale(1./lower_data.Integral())
    if(higher_data.Integral() != 0):
        higher_data.Scale(1./higher_data.Integral())


    #cloning for bin size
    higher = higher_quark.Clone("")
    lower = higher_quark.Clone("")
    #setting bin content for cloned bins
    for i in range(1,higher.GetNbinsX()+1):
        higher.SetBinContent(i,fg*higher_gluon.GetBinContent(i)+fq*higher_quark.GetBinContent(i))
        lower.SetBinContent(i,cg*lower_gluon.GetBinContent(i)+cq*lower_quark.GetBinContent(i))
        pass

    quark = higher_quark.Clone("")
    gluon = higher_quark.Clone("")
    quark_data = higher_data.Clone("")
    gluon_data = higher_data.Clone("")


    # Matrix method 

    # Simulation 
    for i in range(1,higher.GetNbinsX()+1):
        F = higher.GetBinContent(i)
        C = lower.GetBinContent(i)
        if((cg*fq-fg*cq) != 0 ):
            Q = -(C*fg-F*cg)/(cg*fq-fg*cq)
            G = (C*fq-F*cq)/(cg*fq-fg*cq)
            quark.SetBinContent(i,Q)
            gluon.SetBinContent(i,G)
        pass
    # Data
    for i in range(1,higher_data.GetNbinsX()+1):
        F = higher_data.GetBinContent(i)
        C = lower_data.GetBinContent(i)
        if((cg*fq-fg*cq) != 0):
            Q = -(C*fg-F*cg)/(cg*fq-fg*cq)
            G = (C*fq-F*cq)/(cg*fq - fg*cq)
            quark_data.SetBinContent(i,Q)
            gluon_data.SetBinContent(i,G)
        pass

    # plotting
    gPad.SetLeftMargin(0.15)
    gPad.SetTopMargin(0.05)
    gPad.SetBottomMargin(0.15)

    if "SF" in mc:
        quark_ratio = quark_data.Clone("")
        gluon_ratio = gluon_data.Clone("")
        quark_ratio.GetYaxis().SetTitle("Data/MC") #Data/MC
        gluon_ratio.GetYaxis().SetTitle("Data/MC") #Data/MC
    if "MC" in mc:
        quark_ratio = higher_quark.Clone("")
        gluon_ratio = higher_gluon.Clone("")
        quark_ratio.GetYaxis().SetTitle("MC Closure") #Data/MC
        gluon_ratio.GetYaxis().SetTitle("MC Closure") #Data/MC

    quark_ratio.Divide(quark)
    gluon_ratio.Divide(gluon)


    gStyle.SetOptStat(0)
    ######################## for ratio plot
    c.Divide(2,1)
    # sets parameters for graph
    def setTopBottom(q,pad1,pad2,pad3,pad4,color,mode,size,tickx,ticky,lMargin,rMargin,bMargin,BorderMode):  
        q.SetPad(pad1,pad2,pad3,pad4)
        q.SetFillColor(color)
        q.SetBorderMode(mode)
        q.SetTickx(tickx)
        q.SetTicky(ticky)
        q.SetLeftMargin(lMargin)
        q.SetRightMargin(rMargin)
        q.SetBottomMargin(bMargin)
        q.SetFrameBorderMode(BorderMode)

    top = c.cd(1)
    setTopBottom(top,0.0,0.0,1.0,1.0,0,0,2,1,1,0.14,0.055,0.3,0)
    bot = c.cd(2)
    bot.SetTopMargin(0.045)
    setTopBottom(bot,0.0,0.0,1.0,0.3,0,0,2,1,1,0.14,0.055,0.4,0)

    # set parameters for graph lines/markers
    def graphMarkers(variable,markColor,lineColor,markSize,markStyle):
        variable.SetMarkerColor(markColor)
        variable.SetLineColor(lineColor)
        variable.SetMarkerSize(markSize)
        variable.SetMarkerStyle(markStyle)
        
    quark.SetTitle("")
    quark.GetXaxis().SetTitle(var)
    quark.GetYaxis().SetTitle("Normalized to unity")
    quark.GetYaxis().SetNdivisions(505)
    quark.GetYaxis().SetRangeUser(-0.01,quark.GetMaximum()*1.5)

    graphMarkers(quark,8,8,0.5,20)
    graphMarkers(quark_data,1,1,0.8,29)
    graphMarkers(higher_quark,2,2,0.5,21)
    graphMarkers(lower_quark,4,4,0.5,22)

    quark_ratio.SetTitle("")
    quark_ratio.GetYaxis().SetRangeUser(0.7,1.3)
    quark_ratio.GetXaxis().SetTitle(var)
    quark_ratio.GetXaxis().SetTitleOffset(1)
    quark_ratio.GetXaxis().SetTitleSize(0.11)
    quark_ratio.GetXaxis().SetLabelSize(0.1)
    quark_ratio.GetXaxis().SetLabelOffset(0.03)
    quark_ratio.GetYaxis().SetTitleSize(0.1)
    quark_ratio.GetYaxis().SetTitleOffset(0.5)
    quark_ratio.GetYaxis().SetLabelOffset(0.01)

    top.cd()
    quark.Draw()
    if "SF" in mc:
		quark_data.Draw("same")
    if "MC" in mc:
         higher_quark.Draw("same")
    if "bdt" in inputvar:
        leg = TLegend(0.75,0.57,0.94,0.67)
        line = TLine(-0.8,1,0.7,1)
    if "ntrk" in inputvar:
        leg = TLegend(0.55,0.55,0.82,0.65)
        line = TLine(0,1,60,1)
    
    # set parameters for legend
    def legFormat(textFont,FillColor,BorderSize,FillStyle,NColumns):
        leg.SetTextFont(textFont)
        leg.SetFillColor(FillColor)
        leg.SetBorderSize(BorderSize)
        leg.SetFillStyle(0)
        leg.SetNColumns(NColumns)
    legFormat(42,0,0,0,1)
    leg.AddEntry(quark,"Extracted quark (mc)","p")

    if "SF" in mc:
        myText(0.18,0.84,"#it{#bf{#scale[1.8]{#bf{ATLAS} Internal}}}")
        leg.AddEntry(quark_data,"Extracted quark (data)","p")
    if "MC" in mc:
        leg.AddEntry(higher_quark,"gamma quark (mc)","p")
        myText(0.18,0.84,"#it{#bf{#scale[1.8]{#bf{ATLAS} Simulation Internal}}}")
    leg.Draw()

    myText(0.18,0.80,"#bf{#scale[1.5]{#sqrt{s} = 13 TeV}}")
    myText(0.18,0.75,"#bf{#scale[1.5]{pT range: "+str(min)+" - "+str(max)+" GeV}}")

    bot.cd()
    quark_ratio.Draw()
    line.Draw("same")

    c.Print("./plots/gamma+/2d1g/plots_"+var+"/quark/quark_"+str(min)+"_"+str(doreweight)+"_"+mc+"_"+var+".pdf")

    gluon.SetTitle("")
    gluon.GetXaxis().SetTitle(var)
    gluon.GetYaxis().SetTitle("Normalized to unity")
    gluon.GetYaxis().SetNdivisions(505)
    gluon.GetYaxis().SetRangeUser(-0.01,gluon.GetMaximum()*1.75)
    graphMarkers(gluon,8,8,0.5,20)
    graphMarkers(gluon_data,1,1,0.8,29)
    graphMarkers(higher_gluon,2,2,0.5,21)
    graphMarkers(lower_gluon,4,4,0.5,22)

    gluon_ratio.SetTitle("")
    gluon_ratio.GetYaxis().SetRangeUser(0.7,1.3)
    gluon_ratio.GetXaxis().SetTitle(var)
    gluon_ratio.GetXaxis().SetTitleOffset(1)
    gluon_ratio.GetXaxis().SetTitleSize(0.11)
    gluon_ratio.GetXaxis().SetLabelSize(0.1)
    gluon_ratio.GetXaxis().SetLabelOffset(0.03)
    gluon_ratio.GetYaxis().SetTitleSize(0.1)
    gluon_ratio.GetYaxis().SetTitleOffset(0.5)
    gluon_ratio.GetYaxis().SetLabelOffset(0.01)

    top.cd()
    gluon.Draw()
    if "SF" in mc:
        gluon_data.Draw("same")
    if "MC" in mc:
        higher_gluon.Draw("same")

    if "bdt" in inputvar:
        leg = TLegend(0.15,0.55,0.42,0.65)
        line = TLine(-0.8,1,0.7,1)
    if "ntrk" in inputvar:
        leg = TLegend(0.55,0.55,0.82,0.65)
        line = TLine(0,1,60,1)##0.6,0.5,0.9,0.7
  
    legFormat(42,0,0,0,1)
    
    leg.AddEntry(gluon,"Extracted gluon (mc)","p")
    if "SF" in mc:
        leg.AddEntry(gluon_data,"Extracted gluon (data)","p")
        myText(0.18,0.84,"#it{#bf{#scale[1.8]{#bf{ATLAS} Internal}}}")
    if "MC" in mc:
        myText(0.18,0.84,"#it{#bf{#scale[1.8]{#bf{ATLAS} Simulation Internal}}}")
        leg.AddEntry(higher_gluon,"gamma gluon (mc)","p")
    leg.Draw()

    myText(0.18,0.80,"#bf{#scale[1.5]{#sqrt{s} = 13 TeV}}")
    myText(0.18,0.75,"#bf{#scale[1.5]{pT range: "+str(min)+" - "+str(max)+" GeV}}")

    bot.cd()
    gluon_ratio.Draw()
    line.Draw("same")
    c.Print("./plots/gamma+/2d1g/plots_"+var+"/gluon/gluon_"+str(min)+"_"+str(doreweight)+"_"+mc+"_"+var+".pdf")
