# General purpose imports to handle paths, files etc
import os
import os.path as op
import nibabel as nib

#General libraries for data manipulation
import pandas as pd
import numpy as np

# Useful imports to define the direct download function below
import urllib.request
from tqdm import tqdm


class FlankerTest():
    """
    This class is used to bind the data and its associated function used for the analysis of the Flanker test. It is very important as it reduces complexity, abstracts, and generalizes data. 
    """
    
    AC_NUMBER = 'ds000102'
    VERSION = '00001'
    BIDS_ROOT = op.join(os.path.expanduser('~'), 'mne_data')
    
    def __init__(self, subject):        
        #subject ID
        self.subject = subject 
        
        #define folder paths according to BIDS
        self.folder_paths()        
        
    def folder_paths(self):  
        """
        Creates the folders and sets the paths
        """
        # Define folder paths
        self.FUNC_PATH = op.join(self.BIDS_ROOT, self.AC_NUMBER, self.subject, 'func')
        self.ANAT_PATH = op.join(self.BIDS_ROOT, self.AC_NUMBER, self.subject, 'anat')
        self.DER_ANAT_PATH = op.join(self.BIDS_ROOT, self.AC_NUMBER, 'derivatives', self.subject, 'anat')
        self.DER_FUNC_PATH = op.join(self.BIDS_ROOT, self.AC_NUMBER, 'derivatives', self.subject, 'func')
        
        #create directories in BIDS format
        self.mkdir_no_exist(self.BIDS_ROOT)
        self.mkdir_no_exist(self.ANAT_PATH)
        self.mkdir_no_exist(self.FUNC_PATH)
        self.mkdir_no_exist(self.DER_ANAT_PATH)
        self.mkdir_no_exist(self.DER_FUNC_PATH)
        
    def download_open_neuro(self, anat=True, func=True):
        """
        Saves the file names and calls the function to download the dataset
        """
        self.file_list = []
        self.file_types = []
        self.save_dirs = []
        
        if anat:
            self.file_list += [self.subject+'_T1w.nii.gz']
            self.file_types += ['anat']
            self.save_dirs += [self.ANAT_PATH]
        if func:
            self.file_list += [self.subject+'_task-flanker_run-1_bold.nii.gz',
                               self.subject+'_task-flanker_run-1_events.tsv',
                               self.subject+'_task-flanker_run-2_bold.nii.gz',
                               self.subject+'_task-flanker_run-2_events.tsv']
            self.file_types += ['func']*4
            self.save_dirs += [self.FUNC_PATH]*4
        
        #download files from openneuro
        self.direct_file_download_open_neuro(file_list=self.file_list,
                                             file_types=self.file_types,
                                             dataset_id=self.AC_NUMBER,
                                             dataset_version=self.VERSION,
                                             save_dirs=self.save_dirs)
    
    def mkdir_no_exist(self, path):
        """
        Creates a folder if not already created
        """
        if not op.isdir(path):
            os.makedirs(path)

    def download_url(self, url, output_path):
        """
        Download the data from an url
        """
        with self.DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1]) as t:
            urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

    def direct_file_download_open_neuro(self, file_list, file_types, dataset_id, dataset_version, save_dirs):
        """
        Taken from Lab2: Download the dataset from the openneuro website
        """
        # https://openneuro.org/crn/datasets/ds000102/snapshots/00001/files/sub-01:func:sub-01_task-flanker_run-1_bold.nii.gz
        for i, n in enumerate(file_list):
            subject = n.split('_')[0]
            download_link = 'https://openneuro.org/crn/datasets/{}/snapshots/{}/files/{}:{}:{}'.format(dataset_id, dataset_version, subject, file_types[i],n)
            print('Attempting download from ', download_link)
            self.download_url(download_link, op.join(save_dirs[i], n))
            print('Ok')
    
    def framewise_displacement(self, path):
        """
        Taken from Lab2: Computes the framewise displacement
        """
        mot_params = pd.read_csv(path, sep='  ', header=None, engine='python', 
                                                              names=['Rotation x', 
                                                              'Rotation y', 
                                                              'Rotation z',
                                                              'Translation x', 
                                                              'Translation y', 
                                                              'Translation z'])
        framewise_diff = mot_params.diff().iloc[1:]

        rot_params = framewise_diff[['Rotation x', 'Rotation y', 'Rotation z']]  
        converted_rots = rot_params*50 # Estimating displacement on a 50mm radius sphere
        trans_params = framewise_diff[['Translation x', 'Translation y', 'Translation z']]
        fd = converted_rots.abs().sum(axis=1) + trans_params.abs().sum(axis=1)
        
        return fd
    
    def compute_DVARS(self, path):
        """
        Computes the DVARS to detect the volumes with large motion
        """
        data = nib.load(path).get_fdata()
        return np.mean(np.diff(data, axis=3)**2, axis=(0,1,2))**(1/2)
        

    class DownloadProgressBar(tqdm):
        """
        Taken from Lab2: Shows the progressbar on the terminal
        """
        def update_to(self, b=1, bsize=1, tsize=None):
            if tsize is not None:
                self.total = tsize
            self.update(b * bsize - self.n)  
    
    
def reset_overlays():
    """
    Clears view and completely remove visualization. All files opened in FSLeyes are closed.
    The view (along with any color map) is reset tFo the regular ortho panel.
    """
    l = frame.overlayList
    while(len(l)>0):
        del l[0]
    frame.removeViewPanel(frame.viewPanels[0])
    # Put back an ortho panel in our viz for future displays
    frame.addViewPanel(OrthoPanel)