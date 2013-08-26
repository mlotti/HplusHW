#!/bin/bash

rm -f histograms-165970-167913.root histograms-170722-173692.root histograms-170722-172619.root histograms-172620-173692.root 

hadd histograms-165970-167913.root {Tau_Single_165970-166164_Prompt,Tau_Single_166346-166346_Prompt,Tau_Single_166374-167043_Prompt,Tau_Single_167078-167913_Prompt}/res/histograms_*.root

hadd histograms-170722-173692.root {Tau_Single_170722-172619_Aug05,Tau_Single_172620-173198_Prompt,Tau_Single_173236-173692_Prompt}/res/histograms_*.root
hadd histograms-170722-172619.root Tau_Single_170722-172619_Aug05/res/histograms_*.root
hadd histograms-172620-173692.root {Tau_Single_172620-173198_Prompt,Tau_Single_173236-173692_Prompt}/res/histograms_*.root
