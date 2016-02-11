This readme file contains the technical details about the QCD measurement

1) Minimum set of histograms required for doing the QCD measurement:
- MET histograms at the point of normalization for both inverted and baseline
- Shape histograms at the end of the inverted leg

2) Common plots (i.e. the input for the data-driven histograms)
- The common plots histograms need to be filled in the inverted leg
  (in pseudomulticrab creator the proper normalization is applied to them)

3) Normalization
- Determines normalization from the MET histograms at the point of normalization
  using input from both inverted and baseline legs
- Determines combined normalization coefficients by looking at the amount of
  QCD and EWK fake tau events in the shape histograms at the end of the inverted leg

4) Uncertainty for combining the QCD and EWK fake tau normalization coefficients
- This is done by calculating the uncertainty on the combined norm. coefficient
  and by varying it up and down by 1 sigma (done in pseudomulticrab creator)

5) MET shape uncertainty, i.e. how the normalization impacts the final shape
- This is calculated in the pseudomulticrab creator
- As input one needs shape histograms at the point of normalization for both
  the inverted and baseline legs. The details are in
  ../python/systematicsForMetShapeDifference.py
- To add the MET shape uncertainty also to the data driven control plots, one
  needs to add two further sets of CommonPlots histograms: both filled at the
  point of normalization, one for the inverted leg and one for the baseline leg

6) Proper scaling of the shape uncertainties affecting MC EWK genuine taus
- The varying does the scaling automatically, i.e. no further scaling is needed.

7) Proper scaling of the scalar uncertainties affecting MC EWK genuine taus
- As input, one needs to know the fraction of MC EWK genuine taus at the point where
  each of the CommonPlots histograms and shape histograms is created. In practice,
  this is done by calculating the QCD+fake purity, i.e. 
    (N_data - N_MC_EWK_genuine_taus) / N_data .
- This purity needs to be calculated as a function of the shape in question;
  although usually just the overall purity is used 
  (i.e. sum_i (N_i*purity_i) / sum_i (N_i))
- In practice, the pseudomulticrab creator calculates such purity histograms
- In the datacard generator, the information of the purity histogram is then used
  to assign a scalar uncertainty based on the amount of MC EWK genuine taus
  according to:
    -(1-purity)*uncertainty
- For example, if the luminosity uncertainty is 2.6% and the fraction of QCD and
  fake events is 70% at the end of the inverted selection, then the proper scaled
  uncertainty to be assigned for the QCD measurement for luminosity (i.e. affecting
  only the impurity of subtracted MC EWK genuine tau events) should be
    -(1-0.7)*2.6% = -0.3*2.6% = -0.8%
- Check that the obtained scaled scalar uncertainties are anti-correlated with
  those from signal analysis, i.e. for example -0.8 % for luminosity uncertainty.
  The anti-correlation is known to improve the actual limits.
