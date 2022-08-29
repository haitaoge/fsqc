"""
This module provides a function to create surface plots

"""

# -----------------------------------------------------------------------------

def createSurfacePlots(SUBJECT, SUBJECTS_DIR, SURFACES_OUTDIR, VIEWS):

    """
    function createSurfacePlots

    requires the python kaleido package ("pip3 install --user -U kaleido")

    """

    # -----------------------------------------------------------------------------
    # imports

    import os
    import numpy as np
    import nibabel as nb
    import lapy as lp
    from lapy import Plot as lpp
    from lapy import TriaIO as lpio

    # -----------------------------------------------------------------------------
    # settings
    _views_available = [('anterior', 0,2,0), ('posterior', 0,-2,0), ('left', -2,0,0), ('right', 2,0,0), ('superior', 0,0,2), ('inferior', 0,0,-2)] 
    scale_png = 0.8
    # -----------------------------------------------------------------------------
    # import surfaces and overlays

    triaPialL = lpio.import_fssurf(os.path.join(SUBJECTS_DIR, SUBJECT, 'surf', 'lh.pial'))
    triaPialR = lpio.import_fssurf(os.path.join(SUBJECTS_DIR, SUBJECT, 'surf', 'rh.pial'))
    triaInflL = lpio.import_fssurf(os.path.join(SUBJECTS_DIR, SUBJECT, 'surf', 'lh.inflated'))
    triaInflR = lpio.import_fssurf(os.path.join(SUBJECTS_DIR, SUBJECT, 'surf', 'rh.inflated'))

    annotL = nb.freesurfer.read_annot(os.path.join(SUBJECTS_DIR, SUBJECT, 'label', 'lh.aparc.annot'), orig_ids=False)
    annotR = nb.freesurfer.read_annot(os.path.join(SUBJECTS_DIR, SUBJECT, 'label', 'rh.aparc.annot'), orig_ids=False)

    # -----------------------------------------------------------------------------
    # plots

    # check if annotation has labels that are not included in the colortable
    if any(annotL[0]==-1):
        # prepend colortable and update indices
        ctabL = np.concatenate((np.mat([127, 127, 127]), annotL[1][:,0:3]), axis=0)
        indsL = annotL[0] + 1
    else:
        ctabL = annotL[1][:,0:3]
        indsL = annotL[0]

    vAnnotL = ctabL[indsL,:]

    # check if annotation has labels that are not included in the colortable
    if any(annotR[0]==-1):
        # prepend colortable and update indices
        ctabR = np.concatenate((np.mat([127, 127, 127]), annotR[1][:,0:3]), axis=0)
        indsR = annotR[0] + 1
    else:
        ctabR = annotR[1][:,0:3]
        indsR = annotR[0]

    vAnnotR = ctabR[indsR,:]

    # -----------------------------------------------------------------------------
    # plots
    
    for view, x,y,z in _views_available:
        fpath_lp = os.path.join(SURFACES_OUTDIR, f'lh.pial.{view}.png')
        fpath_rp = os.path.join(SURFACES_OUTDIR, f'rh.pial.{view}.png')
        fpath_li = os.path.join(SURFACES_OUTDIR, f'lh.inflated.{view}.png')
        fpath_ri = os.path.join(SURFACES_OUTDIR, f'rh.inflated.{view}.png')
        
        if view in VIEWS:
            camera = dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=x, y=y, z=z))

            lpp.plot_tria_mesh(triaPialL, vcolor=vAnnotL, background_color="black", camera=camera, export_png=fpath_lp, no_display=True, scale_png=scale_png)
            lpp.plot_tria_mesh(triaPialR, vcolor=vAnnotR, background_color="black", camera=camera, export_png=fpath_rp, no_display=True, scale_png=scale_png)
            lpp.plot_tria_mesh(triaInflL, vcolor=vAnnotL, background_color="black", camera=camera, export_png=fpath_li, no_display=True, scale_png=scale_png)
            lpp.plot_tria_mesh(triaInflR, vcolor=vAnnotR, background_color="black", camera=camera, export_png=fpath_ri, no_display=True, scale_png=scale_png)
        else:
            # remove images potentially created in earlier run but not updated now
            for fpath in [fpath_lp, fpath_rp, fpath_li, fpath_ri]:
                if os.path.isfile(fpath):
                    os.remove(fpath)
