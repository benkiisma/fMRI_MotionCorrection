# fMRI_MotionCorrection

The quality of fMRI data is affected by the subject’s motion in the scanner. This can cause signal alterations across fMRI volumes generating spurious results. Hence, motion correction is always an important preprocessing step in fMRI data analysis. This code will perform brain extraction and motion correction to fMRI acquired data. 
The dataset that I used is accessible through openneuroi: Flanker test https://openneuro.org/datasets/ds000102/versions/00001.


### Directory structure
```

│   README.md
│   main.ipynb
│   utils.py
│   
├───images
        bet_skull.png
        fMRI_Tmean.png
        static_visualization.png   
        sub-01_animation.gif
        sub-01_run-1_animation.gif
        sub-01_run-1_moco_animation.gif
        thresholding.png
        voxel_timeseries.png
```

To start the notebook, run the following line on a terminal :

    fsleyes --notebookFile main.ipynb
    
### Dependencies
- os
- nibabel
- pandas
- numpy
- tqdm
- urllib
- matplotlib
- FSLPy
- Nilearn
- Dipy 
- MNE-NIRS 
- jupyterlab
- openneuro-py 
- fsleyes

### Data 
The data can be found here : https://openneuro.org/datasets/ds000102/versions/00001 \
It comprises data collected from 26 healthy adults while they performed a slow event-related Eriksen Flanker task. For this study, only the first three subjects are used (sub-01, sub-02, sub-03). 

### References
Kelly, A.M., Uddin, L.Q., Biswal, B.B., Castellanos, F.X., Milham, M.P. (2008). Competition between functional brain networks mediates behavioral variability. Neuroimage, 39(1):527-37

Mennes, M., Kelly, C., Zuo, X.N., Di Martino, A., Biswal, B.B., Castellanos, F.X., Milham, M.P. (2010). Inter-individual differences in resting-state functional connectivity predict task-induced BOLD activity. Neuroimage, 50(4):1690-701. doi: 10.1016/j.neuroimage.2010.01.002. Epub 2010 Jan 15. Erratum in: Neuroimage. 2011 Mar 1;55(1):434

Mennes, M., Zuo, X.N., Kelly, C., Di Martino, A., Zang, Y.F., Biswal, B., Castellanos, F.X., Milham, M.P. (2011). Linking inter-individual differences in neural activation and behavior to intrinsic brain dynamics. Neuroimage, 54(4):2950-9. doi: 10.1016/j.neuroimage.2010.10.046
