"""
This module provides the main functionality of the qatoolspython package.

"""

# ==============================================================================
# FUNCTIONS

# ------------------------------------------------------------------------------
# get_help()


def get_help(print_help=True, return_help=False):
    """
    a function to return a help message

    """

    HELPTEXT = """

    qatools-python


    ============
    Description:
    ============

    This is a set of quality assurance / quality control scripts for Fastsurfer-
    or Freesurfer-processed structural MRI data.

    It is a revision, extension, and translation to the Python language of the
    original Freesurfer QA Tools that are provided at
    https://surfer.nmr.mgh.harvard.edu/fswiki/QATools

    It has been augmented by additional functions from the MRIQC toolbox, available
    at https://github.com/poldracklab/mriqc and https://osf.io/haf97, and with code
    derived from the shapeDNA and brainPrint toolboxes, available at
    https://reuter.mit.edu.

    The core functionality of this toolbox is to compute the following features:

    - wm_snr_orig   ...  signal-to-noise for white matter in orig.mgz
    - gm_snr_orig   ...  signal-to-noise for gray matter in orig.mgz
    - wm_snr_norm   ...  signal-to-noise for white matter in norm.mgz
    - gm_snr_norm   ...  signal-to-noise for gray matter in norm.mgz
    - cc_size       ...  relative size of the corpus callosum
    - holes_lh      ...  number of holes in the left hemisphere
    - holes_rh      ...  number of holes in the right hemisphere
    - defects_lh    ...  number of defects in the left hemisphere
    - defects_rh    ...  number of defects in the right hemisphere
    - topo_lh       ...  topological fixing time for the left hemisphere
    - topo_rh       ...  topological fixing time for the right hemisphere
    - con_snr_lh    ...  wm/gm contrast signal-to-noise ratio in the left hemisphere
    - con_snr_rh    ...  wm/gm contrast signal-to-noise ratio in the right hemisphere
    - rot_tal_x     ...  rotation component of the Talairach transform around the x axis
    - rot_tal_y     ...  rotation component of the Talairach transform around the y axis
    - rot_tal_z     ...  rotation component of the Talairach transform around the z axis

    The program will use an existing output directory (or try to create it) and
    write a csv table into that location. The csv table will contain the above
    metrics plus a subject identifier.

    In addition to the core functionality of the toolbox there are several optional
    modules that can be run according to need:

    - screenshots module

    This module allows for the automated generation of cross-sections of the brain
    that are overlaid with the anatomical segmentations (asegs) and the white and
    pial surfaces. These images will be saved to the 'screenshots' subdirectory
    that will be created within the output directory. These images can be used for
    quickly glimpsing through the processing results. Note that no display manager
    is required for this module, i.e. it can be run on a remote server, for example.

    - surfaces module

    This module allows for the automated generation of surface renderings of the
    left and right pial and inflated surfaces, overlaid with the aparc annotation.
    These images will be saved to the 'surfaces' subdirectory that will be created
    within the output directory.

    - skullstrip module

    This module allows for the automated generation cross-sections of the brain
    that are overlaid with the colored and semi-transparent brainmask. this allows
    to check the quality of the skullstripping in FreeSurfer. The resulting images
    will be saved to the 'skullstrip' subdirectory that will be created within the
    output directory.

    - fornix module

    This is a module to assess potential issues with the segmentation of the
    corpus callosum, which may incorrectly include parts of the fornix. To assess
    segmentation quality, a screenshot of the contours of the corpus callosum
    segmentation overlaid on the norm.mgz will be saved in the 'fornix'
    subdirectory of the output directory.

    - modules for the amygdala, hippocampus, and hypothalamus

    These modules evaluate potential missegmentations of the amygdala, hippocampus,
    and hypothalamus. To assess segmentation quality, screenshots will be created
    These modules require prior processing of the MR images with FreeSurfer's
    dedicated toolboxes for the segmentation of the amygdala and hippocampus, and
    the hypothalamus, respectively.

    - shape module

    The shape module will run a shapeDNA / brainprint analysis to compute distances
    of shape descriptors between lateralized brain structures. This can be used
    to identify discrepancies and irregularities between pairs of corresponding
    structures. The results will be included in the main csv table, and the output
    directory will also contain a "brainprint" subdirectory.

    - outlier module

    This is a module to detect extreme values among the subcortical ('aseg')
    segmentations as well as the cortical parcellations ('aparc'). If present,
    hypothalamic and hippocampal subsegmentations will also be included.

    The outlier detection is based on comparisons with the distributions of the
    sample as well as normative values taken from the literature (see References).

    For comparisons with the sample distributions, extreme values are defined in
    two ways: nonparametrically, i.e. values that are 1.5 times the interquartile
    range below or above the 25th or 75th percentile of the sample, respectively,
    and parametrically, i.e. values that are more than 2 standard deviations above
    or below the sample mean. Note that a minimum of 5 supplied subjects is
    required for running these analyses, otherwise `NaNs` will be returned.

    For comparisons with the normative values, lower and upper bounds are computed
    from the 95% prediction intervals of the regression models given in Potvin et
    al., 1996, and values exceeding these bounds will be flagged. As an
    alternative, users may specify their own normative values by using the
    '--outlier-table' argument. This requires a custom csv table with headers
    `label`, `upper`, and `lower`, where `label` indicates a column of anatomical
    names. It can be a subset and the order is arbitrary, but naming must exactly
    match the nomenclature of the 'aseg.stats' and/or '[lr]h.aparc.stats' file.
    If cortical parcellations are included in the outlier table for a comparison
    with aparc.stats values, the labels must have a 'lh.' or 'rh.' prefix.
    `upper` and `lower` are user-specified upper and lower bounds.

    The main csv table will be appended with the following summary variables, and
    more detailed output about will be saved as csv tables in the 'outliers'
    subdirectory of the main output directory.

    n_outliers_sample_nonpar ... number of structures that are 1.5 times the IQR
                                 above/below the 75th/25th percentile
    n_outliers_sample_param  ... number of structures that are 2 SD above/below
                                 the mean
    n_outliers_norms         ... number of structures exceeding the upper and
                                 lower bounds of the normative values


    ======
    Usage:
    ======

        python3 qatools.py --subjects_dir <directory> --output_dir <directory>
                                  [--subjects SubjectID [SubjectID ...]]
                                  [--subjects-file <file>]
                                  [--screenshots] [--screenshots-html]
                                  [--surfaces] [--surfaces-html]
                                  [--skullstrip] [--skullstrip-html]
                                  [--fornix] [--fornix-html] [--hypothalamus]
                                  [--hypothalamus-html] [--hippocampus]
                                  [--hippocampus-html] [--hippocampus-label <label>]
                                  [--shape] [--outlier] [--fastsurfer] [-h]

        required arguments:
          --subjects_dir <directory>
                                subjects directory with a set of Freesurfer-  or
                                Fastsurfer-processed individual datasets.
          --output_dir <directory>
                                output directory

        optional arguments:
          --subjects SubjectID [SubjectID ...]
                                list of subject IDs
          --subjects-file <file>
                                filename of a file with subject IDs (one per line)
          --screenshots         create screenshots of individual brains
          --screenshots-html    create screenshots of individual brains and
                                html summary page
          --surfaces            create screenshots of individual brain surfaces
          --surfaces-html       create screenshots of individual brain surfaces
                                and html summary page
          --skullstrip          create screenshots of individual brainmasks
          --skullstrip-html     create screenshots of individual brainmasks and
                                html summary page
          --fornix              check fornix segmentation
          --fornix-html         check fornix segmentation and create html summary
                                page of fornix evaluation
          --hypothalamus        check hypothalamic segmentation
          --hypothalamus-html   check hypothalamic segmentation and create html
                                summary page
          --hippocampus         check segmentation of hippocampus and amygdala
          --hippocampus-html    check segmentation of hippocampus and amygdala
                                and create html summary page
          --hippocampus-label   specify label for hippocampus segmentation files
                                (default: T1.v21). The full filename is then
                                [lr]h.hippoAmygLabels-<LABEL>.FSvoxelSpace.mgz
          --shape               run shape analysis
          --outlier             run outlier detection
          --outlier-table       specify normative values (only in conjunction with
                                --outlier)
          --fastsurfer          use FastSurfer instead of FreeSurfer output

        getting help:
          -h, --help            display this help message and exit
          --more-help           display extensive help message and exit

        expert options:
          --screenshots_base <image>
                                filename of an image that should be used instead of
                                norm.mgz as the base image for the screenshots. Can be
                                an individual file (which would not be appropriate for
                                multi-subject analysis) or can be a file without
                                pathname and with the same filename across subjects
                                within the 'mri' subdirectory of an individual FreeSurfer
                                results directory (which would be appropriate for multi-
                                subject analysis).
          --screenshots_overlay <image>
                                path to an image that should be used instead of
                                aseg.mgz as the overlay image for the screenshots;
                                can also be none. Can be an individual file (which would
                                not be appropriate for multi-subject analysis) or can be
                                a file without pathname and with the same filename across
                                subjects within the 'mri' subdirectory of an individual
                                FreeSurfer results directory (which would be appropriate
                                for multi-subject analysis).
          --screenshots_surf <surf> [<surf> ...]
                                one or more surface files that should be used instead
                                of [lr]h.white and [lr]h.pial; can also be none.
                                Can be one or more individual file(s) (which would not be
                                appropriate for multi-subject analysis) or can be a (list
                                of) file(s) without pathname and with the same filename
                                across subjects within the 'surf' subdirectory of an
                                individual FreeSurfer results directory (which would be
                                appropriate for multi-subject analysis).
          --screenshots_views <view> [<view> ...]
                                one or more views to use for the screenshots in
                                the form of x=<numeric> y=<numeric> and/or
                                z=<numeric>. order does not matter. default views
                                are x=-10 x=10 y=0 z=0.
          --screenshots_layout <rows> <columns>
                                layout matrix for screenshot images


    ========================
    Use as a python package:
    ========================

    As an alternative to their command-line usage, the qc scripts can also be run
    within a pure python environment, i.e. installed and imported as a python
    package.

    Use `import qatoolspython` (or sth. equivalent) to import the package within a
    python environment.

    Use the `run_qatools` function from the `qatoolspython` module to run an analysis:

    `from qatoolspython import qatoolspython`

    `qatoolspython.run_qatools(subjects_dir='/my/subjects/dir', output_dir='/my/output/dir')`

    See `help(qatoolspython)` for further usage info and options.


    =============
    Known Issues:
    =============

    The program will analyze recon-all logfiles, and may fail or return erroneous
    results if the logfile is append by multiple restarts of recon-all runs.
    Ideally, the logfile should therefore consist of just a single, successful
    recon-all run.


    ========
    Authors:
    ========

    - qatools-python: Kersten Diers, Tobias Wolff, and Martin Reuter.
    - Freesurfer QA Tools: David Koh, Stephanie Lee, Jenni Pacheco, Vasanth Pappu,
      and Louis Vinke.
    - shapeDNA and brainPrint toolboxes: Martin Reuter


    ===========
    References:
    ===========

    Esteban O, Birman D, Schaer M, Koyejo OO, Poldrack RA, Gorgolewski KJ; MRIQC:
    Advancing the Automatic Prediction of Image Quality in MRI from Unseen Sites;
    PLOS ONE 12(9):e0184661; doi:10.1371/journal.pone.0184661.

    Wachinger C, Golland P, Kremen W, Fischl B, Reuter M; 2015; BrainPrint: a
    Discriminative Characterization of Brain Morphology; Neuroimage: 109, 232-248;
    doi:10.1016/j.neuroimage.2015.01.032.

    Reuter M, Wolter FE, Shenton M, Niethammer M; 2009; Laplace-Beltrami
    Eigenvalues and Topological Features of Eigenfunctions for Statistical Shape
    Analysis; Computer-Aided Design: 41, 739-755, doi:10.1016/j.cad.2009.02.007.

    Potvin O, Mouiha A, Dieumegarde L, Duchesne S, & Alzheimer's Disease Neuroimaging
    Initiative; 2016; Normative data for subcortical regional volumes over the lifetime
    of the adult human brain; Neuroimage: 137, 9-20;
    doi.org/10.1016/j.neuroimage.2016.05.016

    =============
    Requirements:
    =============

    At least one subject whose structural MR image was processed with Freesurfer
    6.0 or later.

    A Python version >= 3.8 is required to run this script.

    Required packages include (among others) the nibabel and skimage package for
    the core functionality, plus the the matplotlib, pandas, and transform3d
    packages for some optional functions and modules. See the `requirements.txt`
    file for a complete list. Use `pip3 install -r requirements.txt` to install
    these packages.

    For the shape analysis module, the brainprint and lapy packages from
    https://github.com/Deep-MI are required (brainprint version 0.2 or newer,
    lapy version 0.3 or newer).

    This software has been tested on Ubuntu 22.04, CentOS7, and MacOS 10.14.


    ========
    License:
    ========

    This software is licensed under the MIT License, see associated LICENSE file
    for details.

    Copyright (c) 2019 Image Analysis Group, DZNE e.V.

    """

    if print_help:
        print(HELPTEXT)

    if return_help:
        return HELPTEXT


# ------------------------------------------------------------------------------
# parse_arguments


def _parse_arguments():
    """
    an internal function to parse input arguments

    """

    # imports
    import sys
    import argparse

    # parse
    parser = argparse.ArgumentParser(
        description="""
        This program takes existing Freesurfer or Fastsurfer analysis results of
        one or more subjects and computes a set of quality metrics. These will
        be reported in a summary csv table.

        For a description of these metrics, see the gitlab/github page or the
        header section of this script.

        Further modules are available to produce graphical outputs.
        """,
        add_help=False,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "--subjects_dir",
        dest="subjects_dir",
        help="subjects directory with a set of Freesurfer processed individual datasets.",
        metavar="<directory>",
        required=True,
    )
    required.add_argument(
        "--output_dir", dest="output_dir", help="output directory", metavar="<directory>", required=True
    )

    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "--subjects",
        dest="subjects",
        help="list of subject IDs. If omitted, all suitable sub-directories witin the subjects directory will be used.",
        default=None,
        nargs="+",
        metavar="SubjectID",
        required=False,
    )
    optional.add_argument(
        "--subjects-file",
        dest="subjects_file",
        help="filename with list of subject IDs (one per line). If omitted, all suitable sub-directories witin the subjects directory will be used.",
        default=None,
        metavar="<filename>",
        required=False,
    )
    optional.add_argument(
        "--shape", dest="shape", help="run shape analysis", default=False, action="store_true", required=False
    )
    optional.add_argument(
        "--screenshots",
        dest="screenshots",
        help="create screenshots of individual brains",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--screenshots-html",
        dest="screenshots_html",
        help="create screenshots of individual brains with html summary page",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--surfaces",
        dest="surfaces",
        help="create surface plots of individual brains",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--surfaces-html",
        dest="surfaces_html",
        help="create surface plots of individual brains with html summary page",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--surfaces_views",
        dest="surfaces_views",
        help="Specify camera views for surface images. Choose from: anterior, posterior, left, right, superior, inferior",
        default=["left", "right", "superior", "inferior"],
        type=str,
        nargs="+",
        required=False,
    )
    optional.add_argument(
        "--skullstrip",
        dest="skullstrip",
        help="create brainmask plots of individual brains",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--skullstrip-html",
        dest="skullstrip_html",
        help="create brainmask plots of individual brains with html summary page",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--fornix", dest="fornix", help="check fornix segmentation", default=False, action="store_true", required=False
    )
    optional.add_argument(
        "--fornix-html",
        dest="fornix_html",
        help="check fornix segmentation and create html summary page",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--hypothalamus",
        dest="hypothalamus",
        help="check hypothalamus segmentation",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--hypothalamus-html",
        dest="hypothalamus_html",
        help="check hypothalamus segmentation and create html summary page for evaluation",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--hippocampus",
        dest="hippocampus",
        help="check hippocampus segmentation",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--hippocampus-html",
        dest="hippocampus_html",
        help="check hippocampus segmentation and create html summary page for evaluation",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--hippocampus-label",
        dest="hippocampus_label",
        help="specify custom label for hippocampal segmentation files",
        default=None,
        metavar="<string>",
        required=False,
    )
    optional.add_argument(
        "--outlier", dest="outlier", help="run outlier detection", default=False, action="store_true", required=False
    )
    optional.add_argument(
        "--outlier-table",
        dest="outlier_table",
        help="specify normative values",
        default=None,
        metavar="<filename>",
        required=False,
    )
    optional.add_argument(
        "--fastsurfer",
        dest="fastsurfer",
        help="use FastSurfer output",
        default=False,
        action="store_true",
        required=False,
    )

    expert = parser.add_argument_group("expert arguments")
    expert.add_argument(
        "--screenshots_base",
        dest="screenshots_base",
        help="base image for screenshots",
        default="default",
        metavar="<base image for screenshots>",
        required=False,
    )
    expert.add_argument(
        "--screenshots_overlay",
        dest="screenshots_overlay",
        help="overlay image for screenshots",
        default="default",
        metavar="<overlay image for screenshots>",
        required=False,
    )
    expert.add_argument(
        "--screenshots_surf",
        dest="screenshots_surf",
        help="surface(s) for screenshots",
        default="default",
        nargs="+",
        metavar="<surface(s) for screenshots>",
        required=False,
    )
    expert.add_argument(
        "--screenshots_views",
        dest="screenshots_views",
        help="view specification for screenshots",
        default=["x=-10", "x=10", "y=0", "z=0"],
        nargs="+",
        metavar="<dimension=coordinate [dimension=coordinate]>",
        required=False,
    )
    expert.add_argument(
        "--screenshots_layout",
        dest="screenshots_layout",
        help="layout for screenshots",
        default=["1", "4"],
        nargs=2,
        metavar="<num>",
        required=False,
    )
    expert.add_argument(
        "--screenshots_orientation",
        dest="screenshots_orientation",
        help=argparse.SUPPRESS,
        default=["radiological"],
        nargs=1,
        metavar="<neurological|radiological>",
        required=False,
    )  # this is currently a hidden "expert" option

    help = parser.add_argument_group("getting help")
    help.add_argument("-h", "--help", help="display this help message and exit", action="help")
    help.add_argument(
        "--more-help",
        dest="more_help",
        help="display extensive help message and exit",
        default=False,
        action="store_true",
        required=False,
    )

    # check if there are any inputs; if not, print help and exit
    if len(sys.argv) == 1:
        args = parser.parse_args(["--help"])
    elif len(sys.argv) == 2 and sys.argv[1] == "--more-help":
        get_help()
        sys.exit(0)
    else:
        args = parser.parse_args()

    # check for extensive help (if it exists among other arguments)
    if args.more_help:
        get_help()
        sys.exit(0)

    # prepare output
    argsDict = dict()
    argsDict["subjects_dir"] = args.subjects_dir
    argsDict["output_dir"] = args.output_dir
    argsDict["subjects"] = args.subjects
    argsDict["subjects_file"] = args.subjects_file
    argsDict["shape"] = args.shape
    argsDict["screenshots"] = args.screenshots
    argsDict["screenshots_html"] = args.screenshots_html
    argsDict["screenshots_base"] = args.screenshots_base
    argsDict["screenshots_overlay"] = args.screenshots_overlay
    argsDict["screenshots_surf"] = args.screenshots_surf
    argsDict["screenshots_views"] = args.screenshots_views
    argsDict["screenshots_layout"] = args.screenshots_layout
    argsDict["screenshots_orientation"] = args.screenshots_orientation
    argsDict["surfaces"] = args.surfaces
    argsDict["surfaces_html"] = args.surfaces_html
    argsDict["surfaces_views"] = args.surfaces_views
    argsDict["skullstrip"] = args.skullstrip
    argsDict["skullstrip_html"] = args.skullstrip_html
    argsDict["fornix"] = args.fornix
    argsDict["fornix_html"] = args.fornix_html
    argsDict["hypothalamus"] = args.hypothalamus
    argsDict["hypothalamus_html"] = args.hypothalamus_html
    argsDict["hippocampus"] = args.hippocampus
    argsDict["hippocampus_html"] = args.hippocampus_html
    argsDict["hippocampus_label"] = args.hippocampus_label
    argsDict["outlier"] = args.outlier
    argsDict["outlier_table"] = args.outlier_table
    argsDict["fastsurfer"] = args.fastsurfer

    #
    return argsDict


# ------------------------------------------------------------------------------
# check arguments


def _check_arguments(argsDict):
    """
    an internal function to check input arguments

    """

    # --------------------------------------------------------------------------
    # imports

    import os
    import sys
    import errno

    import tempfile
    import importlib.util

    # --------------------------------------------------------------------------
    # check arguments

    # check if subject directory exists
    if os.path.isdir(argsDict["subjects_dir"]):
        print("Found subjects directory", argsDict["subjects_dir"])
    else:
        print("ERROR: subjects directory " + argsDict["subjects_dir"] + " is not an existing directory\n")
        sys.exit(1)

    # check if output directory exists or can be created and is writable
    if os.path.isdir(argsDict["output_dir"]):
        print("Found output directory", argsDict["output_dir"])
    else:
        try:
            os.mkdir(argsDict["output_dir"])
        except:
            print("ERROR: cannot create output directory " + argsDict["output_dir"] + "\n")
            sys.exit(1)

        try:
            testfile = tempfile.TemporaryFile(dir=argsDict["output_dir"])
            testfile.close()
        except OSError as e:
            if e.errno != errno.EACCES:  # 13
                e.filename = argsDict["output_dir"]
                raise
            print("\nERROR: " + argsDict["output_dir"] + " not writeable (check access)!\n")
            sys.exit(1)

    # check if both subjects and subjects-file were specified
    if argsDict["subjects"] is not None and argsDict["subjects_file"] is not None:
        print("ERROR: Use either --subjects or --subjects-file (but not both).")
        sys.exit(1)

    # check if subjects-file exists and get data
    if argsDict["subjects_file"] is not None:
        if os.path.isfile(argsDict["subjects_file"]):
            # read file
            with open(argsDict["subjects_file"]) as subjects_file_f:
                argsDict["subjects"] = subjects_file_f.read().splitlines()
        else:
            print("ERROR: Could not find subjects file", argsDict["subjects_file"])
            sys.exit(1)

    # if neither subjects nor subjects_file are given, get contents of the subject
    # directory and check if aseg.stats (as a proxy) exists
    if argsDict["subjects"] is None and argsDict["subjects_file"] is None:
        argsDict["subjects"] = []
        for subject in os.listdir(argsDict["subjects_dir"]):
            path_aseg_stat = os.path.join(argsDict["subjects_dir"], subject, "stats", "aseg.stats")
            if os.path.isfile(path_aseg_stat):
                print("Found subject", subject)
                argsDict["subjects"].extend([subject])

    # check if screenshots subdirectory exists or can be created and is writable
    if argsDict["screenshots"] is True or argsDict["screenshots_html"] is True:
        if os.path.isdir(os.path.join(argsDict["output_dir"], "screenshots")):
            print("Found screenshots directory", os.path.join(argsDict["output_dir"], "screenshots"))
        else:
            try:
                os.mkdir(os.path.join(argsDict["output_dir"], "screenshots"))
            except:
                print(
                    "ERROR: cannot create screenshots directory "
                    + os.path.join(argsDict["output_dir"], "screenshots")
                    + "\n"
                )
                sys.exit(1)

            try:
                testfile = tempfile.TemporaryFile(dir=os.path.join(argsDict["output_dir"], "screenshots"))
                testfile.close()
            except OSError as e:
                if e.errno != errno.EACCES:  # 13
                    e.filename = os.path.join(argsDict["output_dir"], "screenshots")
                    raise
                print(
                    "\nERROR: "
                    + os.path.join(argsDict["output_dir"], "screenshots")
                    + " not writeable (check access)!\n"
                )
                sys.exit(1)

    # check further screenshots dependencies
    if (argsDict["screenshots"] is True or argsDict["screenshots_html"] is True) and importlib.util.find_spec(
        "pandas"
    ) is None:
        print("\nERROR: the 'pandas' package is required for running this script, please install.\n")
        sys.exit(1)

    if (argsDict["screenshots"] is True or argsDict["screenshots_html"] is True) and importlib.util.find_spec(
        "matplotlib"
    ) is None:
        print("\nERROR: the 'matplotlib' package is required for running this script, please install.\n")
        sys.exit(1)

    # check screenshots_base
    argsDict["screenshots_base"] = [argsDict["screenshots_base"]]

    # check screenshots_overlay (this is either 'default' or 'none' or a single file or a list; further checks prior to execution of the screenshots module)
    if argsDict["screenshots_overlay"].lower() == "none":
        argsDict["screenshots_overlay"] = None
        print("Found screenshot overlays set to None")
    else:
        argsDict["screenshots_overlay"] = [argsDict["screenshots_overlay"]]

    # check screenshots_surf (this is either 'default' or 'none' or a single file or a list; further checks prior to execution of the screenshots module)
    if not isinstance(argsDict["screenshots_surf"], list):
        argsDict["screenshots_surf"] = [argsDict["screenshots_surf"]]
    if argsDict["screenshots_surf"][0].lower() == "none":
        argsDict["screenshots_surf"] = None
        print("Found screenshot surfaces set to None")

    # check if screenshots_views argument can be evaluated
    if argsDict["screenshots_views"] == "default":
        argsDict["screenshots_views"] = [argsDict["screenshots_views"]]
    else:
        for x in argsDict["screenshots_views"]:
            isXYZ = x.split("=")[0] == "x" or x.split("=")[0] == "y" or x.split("=")[0] == "z"
            try:
                int(x.split("=")[1])
                isConvertible = True
            except:
                isConvertible = False
            if not isXYZ or not isConvertible:
                print()
                print("ERROR: could not understand " + x)
                print()
                print(
                    "       the --screenshots_views argument can only contain one or more x=<numeric> y=<numeric> z=<numeric> expressions."
                )
                print()
                print("       for example: --screenshots_views x=0")
                print("                    --screenshots_views x=-10 x=10 y=0")
                print("                    --screenshots_views x=0 z=0")
                print()
                sys.exit(1)

        print("Found screenshot coordinates ", argsDict["screenshots_views"])
        argsDict["screenshots_views"] = [
            (y[0], int(y[1])) for y in [x.split("=") for x in argsDict["screenshots_views"]]
        ]

    # check screenshots_layout
    if argsDict["screenshots_layout"] is not None:
        if all([x.isdigit() for x in argsDict["screenshots_layout"]]):
            argsDict["screenshots_layout"] = [int(x) for x in argsDict["screenshots_layout"]]
        else:
            print("ERROR: screenshots_layout argument can only contain integer numbers\n")
            sys.exit(1)

    # check screenshots_orientation
    if argsDict["screenshots_orientation"] != ["neurological"] and argsDict["screenshots_orientation"] != [
        "radiological"
    ]:
        print("ERROR: screenshots_orientation argument must be either 'neurological' or 'radiological'.\n")
        sys.exit(1)
    else:
        print("Found screenshot orientation set to " + argsDict["screenshots_orientation"][0])

    # check surfaces
    if argsDict["surfaces"] is True or argsDict["surfaces_html"] is True:
        # check for LaPy
        import packaging.version

        if importlib.util.find_spec("lapy") is not None:
            import lapy as lp

            if not hasattr(lp, "__version__"):
                print(
                    "ERROR: Could not determine version of the 'lapy' package (see README.md for details on installation)"
                )
                sys.exit(1)
            elif packaging.version.parse(lp.__version__) < packaging.version.parse("0.3"):
                print(
                    "ERROR: A version >=0.3 of the 'lapy' package is required for surface plots (see README.md for details on installation)"
                )
                sys.exit(1)
        else:
            print("ERROR: Could not find the 'lapy' package (see README.md for details on installation)")
            sys.exit(1)

        # check for kaleido package
        if importlib.util.find_spec("kaleido") is None:
            print(
                "ERROR: Could not find the 'kaleido' package (use e.g. \"pip3 install --user -U kaleido\" to install)"
            )
            sys.exit(1)

    # check if skullstrip subdirectory exists or can be created and is writable
    if argsDict["skullstrip"] is True or argsDict["skullstrip_html"] is True:
        if os.path.isdir(os.path.join(argsDict["output_dir"], "skullstrip")):
            print("Found skullstrip directory", os.path.join(argsDict["output_dir"], "skullstrip"))
        else:
            try:
                os.mkdir(os.path.join(argsDict["output_dir"], "skullstrip"))
            except:
                print(
                    "ERROR: cannot create skullstrip directory "
                    + os.path.join(argsDict["output_dir"], "skullstrip")
                    + "\n"
                )
                sys.exit(1)

            try:
                testfile = tempfile.TemporaryFile(dir=os.path.join(argsDict["output_dir"], "skullstrip"))
                testfile.close()
            except OSError as e:
                if e.errno != errno.EACCES:  # 13
                    e.filename = os.path.join(argsDict["output_dir"], "skullstrip")
                    raise
                print(
                    "\nERROR: "
                    + os.path.join(argsDict["output_dir"], "skullstrip")
                    + " not writeable (check access)!\n"
                )
                sys.exit(1)

    # check if fornix subdirectory exists or can be created and is writable
    if argsDict["fornix"] is True or argsDict["fornix_html"] is True:
        if os.path.isdir(os.path.join(argsDict["output_dir"], "fornix")):
            print("Found fornix directory", os.path.join(argsDict["output_dir"], "fornix"))
        else:
            try:
                os.mkdir(os.path.join(argsDict["output_dir"], "fornix"))
            except:
                print("ERROR: cannot create fornix directory " + os.path.join(argsDict["output_dir"], "fornix") + "\n")
                sys.exit(1)

            try:
                testfile = tempfile.TemporaryFile(dir=os.path.join(argsDict["output_dir"], "fornix"))
                testfile.close()
            except OSError as e:
                if e.errno != errno.EACCES:  # 13
                    e.filename = os.path.join(argsDict["output_dir"], "fornix")
                    raise
                print("\nERROR: " + os.path.join(argsDict["output_dir"], "fornix") + " not writeable (check access)!\n")
                sys.exit(1)

    # check if hypothalamus subdirectory exists or can be created and is writable
    if argsDict["hypothalamus"] is True or argsDict["hypothalamus_html"] is True:
        if os.path.isdir(os.path.join(argsDict["output_dir"], "hypothalamus")):
            print("Found hypothalamus directory", os.path.join(argsDict["output_dir"], "hypothalamus"))
        else:
            try:
                os.mkdir(os.path.join(argsDict["output_dir"], "hypothalamus"))
            except:
                print(
                    "ERROR: cannot create hypothalamus directory "
                    + os.path.join(argsDict["output_dir"], "hypothalamus")
                    + "\n"
                )
                sys.exit(1)

            try:
                testfile = tempfile.TemporaryFile(dir=os.path.join(argsDict["output_dir"], "hypothalamus"))
                testfile.close()
            except OSError as e:
                if e.errno != errno.EACCES:  # 13
                    e.filename = os.path.join(argsDict["output_dir"], "hypothalamus")
                    raise
                print(
                    "\nERROR: "
                    + os.path.join(argsDict["output_dir"], "hypothalamus")
                    + " not writeable (check access)!\n"
                )
                sys.exit(1)

    # check if hippocampus subdirectory exists or can be created and is writable
    if argsDict["hippocampus"] is True or argsDict["hippocampus_html"] is True:
        if os.path.isdir(os.path.join(argsDict["output_dir"], "hippocampus")):
            print("Found hippocampus directory", os.path.join(argsDict["output_dir"], "hippocampus"))
        else:
            try:
                os.mkdir(os.path.join(argsDict["output_dir"], "hippocampus"))
            except:
                print(
                    "ERROR: cannot create hippocampus directory "
                    + os.path.join(argsDict["output_dir"], "hippocampus")
                    + "\n"
                )
                sys.exit(1)

            try:
                testfile = tempfile.TemporaryFile(dir=os.path.join(argsDict["output_dir"], "hippocampus"))
                testfile.close()
            except OSError as e:
                if e.errno != errno.EACCES:  # 13
                    e.filename = os.path.join(argsDict["output_dir"], "hippocampus")
                    raise
                print(
                    "\nERROR: "
                    + os.path.join(argsDict["output_dir"], "hippocampus")
                    + " not writeable (check access)!\n"
                )
                sys.exit(1)

    # check if label file is given
    if (argsDict["hippocampus"] is True or argsDict["hippocampus_html"] is True) and argsDict[
        "hippocampus_label"
    ] is None:
        print(
            "ERROR: The --hippocampus-label <LABEL> argument must be specified if using --hippocampus or --hippocampus-html"
        )
        print(
            "       The filename of the segmentation file must correspond to [lr]h.hippoAmygLabels-<LABEL>.FSvoxelSpace.mgz"
            + "\n"
        )
        sys.exit(1)

    # check if shape subdirectory exists or can be created and is writable
    if argsDict["shape"] is True:
        if os.path.isdir(os.path.join(argsDict["output_dir"], "brainprint")):
            print("Found brainprint directory", os.path.join(argsDict["output_dir"], "brainprint"))
        else:
            try:
                os.makedirs(os.path.join(argsDict["output_dir"], "brainprint"))
            except:
                print(
                    "\nERROR: cannot create brainprint directory "
                    + os.path.join(argsDict["output_dir"], "brainprint")
                    + "\n"
                )
                sys.exit(1)

            try:
                testfile = tempfile.TemporaryFile(dir=os.path.join(argsDict["output_dir"], "brainprint"))
                testfile.close()
            except OSError as e:
                if e.errno != errno.EACCES:  # 13
                    e.filename = os.path.join(argsDict["output_dir"], "brainprint")
                    raise
                print(
                    "\nERROR: "
                    + os.path.join(argsDict["output_dir"], "brainprint")
                    + " not writeable (check access)!\n"
                )
                sys.exit(1)

    # check if shapeDNA / brainPrint dependencies
    if argsDict["shape"] is True:
        # check if brainprintpython can be imported
        if importlib.util.find_spec("brainprint") is None:
            print("\nERROR: could not import the brainprint package, is it installed?")
            sys.exit(1)

        if importlib.util.find_spec("lapy") is None:
            print("\nERROR: could not import the lapy package, is it installed?")
            sys.exit(1)

    # check if outlier subdirectory exists or can be created and is writable
    if argsDict["outlier"] is True:
        if os.path.isdir(os.path.join(argsDict["output_dir"], "outliers")):
            print("Found outliers directory", os.path.join(argsDict["output_dir"], "outliers"))
        else:
            try:
                os.makedirs(os.path.join(argsDict["output_dir"], "outliers"))
            except:
                print(
                    "\nERROR: cannot create outliers directory "
                    + os.path.join(argsDict["output_dir"], "outliers")
                    + "\n"
                )
                sys.exit(1)

            try:
                testfile = tempfile.TemporaryFile(dir=os.path.join(argsDict["output_dir"], "outliers"))
                testfile.close()
            except OSError as e:
                if e.errno != errno.EACCES:  # 13
                    e.filename = os.path.join(argsDict["output_dir"], "outliers")
                    raise
                print(
                    "\nERROR: " + os.path.join(argsDict["output_dir"], "outliers") + " not writeable (check access)!\n"
                )
                sys.exit(1)

    # check if outlier-table exists if it was given, otherwise exit
    if argsDict["outlier_table"] is not None:
        if os.path.isfile(argsDict["outlier_table"]):
            print("Found table with normative values ", argsDict["outlier_table"])
        else:
            print("ERROR: Could not find table with normative values ", argsDict["outlier_table"])
            sys.exit(1)

    # check for required files
    subjects_to_remove = list()
    for subject in argsDict["subjects"]:
        # -files: stats/aseg.stats
        path_check = os.path.join(argsDict["subjects_dir"], subject, "stats", "aseg.stats")
        if not os.path.isfile(path_check):
            print("Could not find", path_check, "for subject", subject)
            subjects_to_remove.extend([subject])

        # -files: surf/[lr]h.w-g.pct.mgh, label/[lr]h.cortex.label
        path_check = os.path.join(argsDict["subjects_dir"], subject, "surf", "lh.w-g.pct.mgh")
        if not os.path.isfile(path_check):
            print("Could not find", path_check, "for subject", subject)
            subjects_to_remove.extend([subject])

        path_check = os.path.join(argsDict["subjects_dir"], subject, "surf", "rh.w-g.pct.mgh")
        if not os.path.isfile(path_check):
            print("Could not find", path_check, "for subject", subject)
            subjects_to_remove.extend([subject])

        path_check = os.path.join(argsDict["subjects_dir"], subject, "label", "lh.cortex.label")
        if not os.path.isfile(path_check):
            print("Could not find", path_check, "for subject", subject)
            subjects_to_remove.extend([subject])

        path_check = os.path.join(argsDict["subjects_dir"], subject, "label", "rh.cortex.label")
        if not os.path.isfile(path_check):
            print("Could not find", path_check, "for subject", subject)
            subjects_to_remove.extend([subject])

        # -files: mri/transforms/talairach.lta
        path_check = os.path.join(argsDict["subjects_dir"], subject, "mri", "transforms", "talairach.lta")
        if not os.path.isfile(path_check):
            print("Could not find", path_check, "for subject", subject)
            subjects_to_remove.extend([subject])

        # -files: mri/norm.mgz, mri/aseg.mgz, mri/aparc+aseg.mgz for FreeSurfer
        # -files: mri/norm.mgz, mri/aseg.mgz, mri/aparc+aseg.orig.mgz for FastSurfer
        path_check = os.path.join(argsDict["subjects_dir"], subject, "mri", "norm.mgz")
        if not os.path.isfile(path_check):
            print("Could not find", path_check, "for subject", subject)
            subjects_to_remove.extend([subject])

        path_check = os.path.join(argsDict["subjects_dir"], subject, "mri", "aseg.mgz")
        if not os.path.isfile(path_check):
            print("Could not find", path_check, "for subject", subject)
            subjects_to_remove.extend([subject])

        if argsDict["fastsurfer"] is True:
            path_check = os.path.join(argsDict["subjects_dir"], subject, "mri", "aparc+aseg.orig.mgz")
        else:
            path_check = os.path.join(argsDict["subjects_dir"], subject, "mri", "aparc+aseg.mgz")
        if not os.path.isfile(path_check):
            print("Could not find", path_check, "for subject", subject)
            subjects_to_remove.extend([subject])

        # -files: scripts/recon-all.log
        path_check = os.path.join(argsDict["subjects_dir"], subject, "scripts", "recon-all.log")
        if not os.path.isfile(path_check):
            print("Could not find", path_check, "for subject", subject)
            subjects_to_remove.extend([subject])

        # check screenshots
        if (argsDict["screenshots"] is True or argsDict["screenshots_html"] is True) and argsDict[
            "screenshots_surf"
        ] == ["default"]:
            # -files: surf/[lr]h.white (optional), surf/[lr]h.pial (optional)
            path_check = os.path.join(argsDict["subjects_dir"], subject, "surf", "lh.white")
            if not os.path.isfile(path_check):
                print("Could not find", path_check, "for subject", subject)
                subjects_to_remove.extend([subject])

            path_check = os.path.join(argsDict["subjects_dir"], subject, "surf", "rh.white")
            if not os.path.isfile(path_check):
                print("Could not find", path_check, "for subject", subject)
                subjects_to_remove.extend([subject])

            path_check = os.path.join(argsDict["subjects_dir"], subject, "surf", "lh.pial")
            if not os.path.isfile(path_check):
                print("Could not find", path_check, "for subject", subject)
                subjects_to_remove.extend([subject])

            path_check = os.path.join(argsDict["subjects_dir"], subject, "surf", "rh.pial")
            if not os.path.isfile(path_check):
                print("Could not find", path_check, "for subject", subject)
                subjects_to_remove.extend([subject])

        # check surfaces
        if argsDict["surfaces"] is True or argsDict["surfaces_html"] is True:
            # -files: surf/[lr]h.white (optional), surf/[lr]h.inflated (optional), label/[lr]h.aparc.annot (optional)
            path_check = os.path.join(argsDict["subjects_dir"], subject, "surf", "lh.inflated")
            if not os.path.isfile(path_check):
                print("Could not find", path_check, "for subject", subject)
                subjects_to_remove.extend([subject])

            path_check = os.path.join(argsDict["subjects_dir"], subject, "surf", "rh.inflated")
            if not os.path.isfile(path_check):
                print("Could not find", path_check, "for subject", subject)
                subjects_to_remove.extend([subject])

            path_check = os.path.join(argsDict["subjects_dir"], subject, "surf", "lh.pial")
            if not os.path.isfile(path_check):
                print("Could not find", path_check, "for subject", subject)
                subjects_to_remove.extend([subject])

            path_check = os.path.join(argsDict["subjects_dir"], subject, "surf", "rh.pial")
            if not os.path.isfile(path_check):
                print("Could not find", path_check, "for subject", subject)
                subjects_to_remove.extend([subject])

            path_check = os.path.join(argsDict["subjects_dir"], subject, "label", "lh.aparc.annot")
            if not os.path.isfile(path_check):
                print("Could not find", path_check, "for subject", subject)
                subjects_to_remove.extend([subject])

            path_check = os.path.join(argsDict["subjects_dir"], subject, "label", "rh.aparc.annot")
            if not os.path.isfile(path_check):
                print("Could not find", path_check, "for subject", subject)
                subjects_to_remove.extend([subject])

        if len(argsDict["surfaces_views"]) > 0:
            _views_available = ["anterior", "posterior", "left", "right", "superior", "inferior"]
            for v in argsDict["surfaces_views"].copy():
                if v not in _views_available:
                    print(f"ERROR: Skip unexpected view for surface plots: {v}")
                    argsDict["surfaces_views"].remove(v)

        # check skullstrip
        if argsDict["skullstrip"] is True or argsDict["skullstrip_html"] is True:
            # -files: surf/[lr]h.white (optional), surf/[lr]h.inflated (optional), label/[lr]h.aparc.annot (optional)
            path_check = os.path.join(argsDict["subjects_dir"], subject, "mri", "orig.mgz")
            if not os.path.isfile(path_check):
                print("Could not find", path_check, "for subject", subject)
                subjects_to_remove.extend([subject])

            path_check = os.path.join(argsDict["subjects_dir"], subject, "mri", "brainmask.mgz")
            if not os.path.isfile(path_check):
                print("Could not find", path_check, "for subject", subject)
                subjects_to_remove.extend([subject])

        # check fornix
        if argsDict["fornix"] is True or argsDict["fornix_html"] is True:
            # -files: mri/transforms/cc_up.lta
            path_check = os.path.join(argsDict["subjects_dir"], subject, "mri", "transforms", "cc_up.lta")
            if not os.path.isfile(path_check):
                print("Could not find", path_check, "for subject", subject)
                subjects_to_remove.extend([subject])

    # remove subjects with missing files after creating unique list
    [argsDict["subjects"].remove(x) for x in list(set(subjects_to_remove))]

    # check if we have any subjects after all
    if not argsDict["subjects"]:
        print("\nERROR: no subjects to process")
        sys.exit(1)

    # now return
    return argsDict


# ------------------------------------------------------------------------------
# check packages


def _check_packages():
    """
    an internal function to check required / recommended packages

    """

    import os
    import sys
    import importlib.util

    if sys.version_info <= (3, 8):
        print("\nERROR: Python version must be 3.8 or greater\n")
        sys.exit(1)

    if importlib.util.find_spec("skimage") is None:
        print("\nERROR: the 'skimage' package is required for running this script, please install.\n")
        sys.exit(1)

    if importlib.util.find_spec("nibabel") is None:
        print("\nERROR: the 'nibabel' package is required for running this script, please install.\n")
        sys.exit(1)

    if importlib.util.find_spec("transforms3d") is None:
        # this package is less important and less standard, so we just return a
        # warning (and NaNs) if it is not found.
        print("\nWARNING: the 'transforms3d' package is recommended, please install.\n")


# ------------------------------------------------------------------------------
# do qatools


def _do_qatools(argsDict):
    """
    an internal function to run the qatools submodules

    """

    # ------------------------------------------------------------------------------
    # imports

    import os
    import csv
    import time

    import numpy as np

    from qatoolspython.checkSNR import checkSNR
    from qatoolspython.checkCCSize import checkCCSize
    from qatoolspython.checkTopology import checkTopology
    from qatoolspython.checkContrast import checkContrast
    from qatoolspython.checkRotation import checkRotation
    from qatoolspython.evaluateFornixSegmentation import evaluateFornixSegmentation
    from qatoolspython.evaluateHypothalamicSegmentation import evaluateHypothalamicSegmentation
    from qatoolspython.evaluateHippocampalSegmentation import evaluateHippocampalSegmentation
    from qatoolspython.createScreenshots import createScreenshots
    from qatoolspython.createSurfacePlots import createSurfacePlots
    from qatoolspython.outlierDetection import outlierTable
    from qatoolspython.outlierDetection import outlierDetection

    # ------------------------------------------------------------------------------
    # internal settings (might be turned into command-line arguments in the future)

    SNR_AMOUT_EROSION = 3
    FORNIX_SCREENSHOT = True
    FORNIX_SHAPE = False
    FORNIX_N_EIGEN = 15
    HYPOTHALAMUS_SCREENSHOT = True
    HIPPOCAMPUS_SCREENSHOT = True
    OUTLIER_N_MIN = 5

    SHAPE_EVEC = False
    SHAPE_SKIPCORTEX = False
    SHAPE_NUM = 50
    SHAPE_NORM = "geometry"
    SHAPE_REWEIGHT = True
    SHAPE_ASYMMETRY = True

    # --------------------------------------------------------------------------
    # process

    # start the processing with a message
    print("")
    print("-----------------------------")

    # create metrics dict
    metricsDict = dict()

    # create images dict
    imagesScreenshotsDict = dict()
    imagesSurfacesDict = dict()
    imagesSkullstripDict = dict()
    imagesFornixDict = dict()
    imagesHypothalamusDict = dict()
    imagesHippocampusLeftDict = dict()
    imagesHippocampusRightDict = dict()

    # create status dict
    statusDict = dict()

    # loop through the specified subjects
    for subject in argsDict["subjects"]:
        #
        print(
            "Starting qatools-python for subject",
            subject,
            "at",
            time.strftime("%Y-%m-%d %H:%M %Z", time.localtime(time.time())),
        )
        print("")

        # ----------------------------------------------------------------------
        # set images

        if argsDict["fastsurfer"] is True:
            aparc_image = "aparc+aseg.orig.mgz"
        else:
            aparc_image = "aparc+aseg.mgz"

        # ----------------------------------------------------------------------
        # add subject to dictionary

        metricsDict.update({subject: {"subject": subject}})
        statusDict.update({subject: {"subject": subject}})

        # ----------------------------------------------------------------------
        # compute core metrics

        # set status
        metrics_ok = True

        # get WM and GM SNR for orig.mgz
        try:
            wm_snr_orig, gm_snr_orig = checkSNR(
                argsDict["subjects_dir"], subject, SNR_AMOUT_EROSION, ref_image="orig.mgz", aparc_image=aparc_image
            )

        except:
            wm_snr_orig = np.nan
            gm_snr_orig = np.nan
            metrics_ok = False

        # get WM and GM SNR for norm.mgz
        try:
            wm_snr_norm, gm_snr_norm = checkSNR(
                argsDict["subjects_dir"], subject, SNR_AMOUT_EROSION, ref_image="norm.mgz", aparc_image=aparc_image
            )

        except:
            wm_snr_norm = np.nan
            gm_snr_norm = np.nan
            metrics_ok = False

        # check CC size
        try:
            cc_size = checkCCSize(argsDict["subjects_dir"], subject)

        except:
            cc_size = np.nan
            metrics_ok = False

        # check topology
        try:
            holes_lh, holes_rh, defects_lh, defects_rh, topo_lh, topo_rh = checkTopology(
                argsDict["subjects_dir"], subject
            )

        except:
            holes_lh = np.nan
            holes_rh = np.nan
            defects_lh = np.nan
            defects_rh = np.nan
            topo_lh = np.nan
            topo_rh = np.nan
            metrics_ok = False

        # check contrast
        try:
            con_snr_lh, con_snr_rh = checkContrast(argsDict["subjects_dir"], subject)

        except:
            con_snr_lh = np.nan
            con_snr_rh = np.nan
            metrics_ok = False

        # check rotation
        try:
            rot_tal_x, rot_tal_y, rot_tal_z = checkRotation(argsDict["subjects_dir"], subject)

        except:
            rot_tal_x = np.nan
            rot_tal_y = np.nan
            rot_tal_z = np.nan
            metrics_ok = False

        # store data
        metricsDict[subject].update(
            {
                "wm_snr_orig": wm_snr_orig,
                "gm_snr_orig": gm_snr_orig,
                "wm_snr_norm": wm_snr_norm,
                "gm_snr_norm": gm_snr_norm,
                "cc_size": cc_size,
                "holes_lh": holes_lh,
                "holes_rh": holes_rh,
                "defects_lh": defects_lh,
                "defects_rh": defects_rh,
                "topo_lh": topo_lh,
                "topo_rh": topo_rh,
                "con_snr_lh": con_snr_lh,
                "con_snr_rh": con_snr_rh,
                "rot_tal_x": rot_tal_x,
                "rot_tal_y": rot_tal_y,
                "rot_tal_z": rot_tal_z,
            }
        )

        # store data
        statusDict[subject].update({"metrics": metrics_ok})

        #
        print("")

        # ----------------------------------------------------------------------
        # run optional modules: shape analysis

        if argsDict["shape"] is True:
            #
            try:
                # message
                print("-----------------------------")
                print("Running brainPrint analysis ...")
                print("")

                # compute brainprint (will also compute shapeDNA)
                from brainprint import brainprint

                # check / create subject-specific brainprint_outdir
                brainprint_outdir = os.path.join(argsDict["output_dir"], "brainprint", subject)

                # run brainPrint
                evMat, evecMat, dstMat = brainprint.run_brainprint(
                    sdir=argsDict["subjects_dir"],
                    sid=subject,
                    outdir=brainprint_outdir,
                    evec=SHAPE_EVEC,
                    skipcortex=SHAPE_SKIPCORTEX,
                    num=SHAPE_NUM,
                    norm=SHAPE_NORM,
                    reweight=SHAPE_REWEIGHT,
                    asymmetry=SHAPE_ASYMMETRY,
                )

                # get a subset of the brainprint results
                distDict = {subject: dstMat}

                # return
                shape_ok = True

                # check / create subject-specific brainprint_outdir
                brainprint_outdir = os.path.join(argsDict["output_dir"], "brainprint", subject)

                # run brainPrint
                evMat, evecMat, dstMat = brainprint.run_brainprint(
                    sdir=argsDict["subjects_dir"],
                    sid=subject,
                    outdir=brainprint_outdir,
                    evec=SHAPE_EVEC,
                    skipcortex=SHAPE_SKIPCORTEX,
                    num=SHAPE_NUM,
                    norm=SHAPE_NORM,
                    reweight=SHAPE_REWEIGHT,
                    asymmetry=SHAPE_ASYMMETRY,
                )

                # get a subset of the brainprint results
                distDict = {subject: dstMat}

                # return
                shape_ok = True

            #
            except:
                distDict = {subject: []}
                print("ERROR: the shape module failed for subject " + subject)
                shape_ok = False

            # store data
            metricsDict[subject].update(distDict[subject])

            # store data
            statusDict[subject].update({"shape": shape_ok})

        # ----------------------------------------------------------------------
        # run optional modules: screenshots

        if argsDict["screenshots"] is True or argsDict["screenshots_html"] is True:
            #
            try:
                # message
                print("-----------------------------")
                print("Creating screenshots ...")
                print("")

                # check / create subject-specific screenshots_outdir
                screenshots_outdir = os.path.join(argsDict["output_dir"], "screenshots", subject)
                if not os.path.isdir(screenshots_outdir):
                    os.makedirs(screenshots_outdir)
                outfile = os.path.join(screenshots_outdir, subject + ".png")

                # re-initialize
                screenshots_base_subj = list()
                screenshots_overlay_subj = list()
                screenshots_surf_subj = list()

                # check screenshots_base
                if argsDict["screenshots_base"][0] == "default":
                    screenshots_base_subj = argsDict["screenshots_base"]
                    print("Using default for screenshot base image")
                elif os.path.isfile(argsDict["screenshots_base"][0]):
                    screenshots_base_subj = argsDict["screenshots_base"]
                    print("Using " + screenshots_base_subj[0] + " as screenshot base image")
                elif os.path.isfile(
                    os.path.join(argsDict["subjects_dir"], subject, "mri", argsDict["screenshots_base"][0])
                ):
                    screenshots_base_subj = [
                        os.path.join(argsDict["subjects_dir"], subject, "mri", argsDict["screenshots_base"][0])
                    ]
                    print("Using " + screenshots_base_subj[0] + " as screenshot base image")
                else:
                    print("\nERROR: cannot find the screenshots base file " + argsDict["screenshots_base"][0] + "\n")
                    sys.exit(1)

                # check screenshots_overlay
                if argsDict["screenshots_overlay"] is not None:
                    if argsDict["screenshots_overlay"][0] == "default":
                        screenshots_overlay_subj = argsDict["screenshots_overlay"]
                        print("Using default for screenshot overlay image")
                    elif os.path.isfile(argsDict["screenshots_overlay"][0]):
                        screenshots_overlay_subj = argsDict["screenshots_overlay"]
                        print("Using " + screenshots_overlay_subj[0] + " as screenshot overlay image")
                    elif os.path.isfile(
                        os.path.join(argsDict["subjects_dir"], subject, "mri", argsDict["screenshots_overlay"][0])
                    ):
                        screenshots_overlay_subj = [
                            os.path.join(argsDict["subjects_dir"], subject, "mri", argsDict["screenshots_overlay"][0])
                        ]
                        print("Using " + screenshots_overlay_subj[0] + " as screenshot overlay image")
                    else:
                        print(
                            "\nERROR: cannot find the screenshots overlay file "
                            + argsDict["screenshots_overlay"][0]
                            + "\n"
                        )
                        sys.exit(1)
                else:
                    screenshots_overlay_subj = argsDict["screenshots_overlay"]

                # check screenshots_surf
                if argsDict["screenshots_surf"] is not None:
                    for screenshots_surf_i in argsDict["screenshots_surf"]:
                        if screenshots_surf_i == "default":
                            print("Using default for screenshot surface")
                        elif os.path.isfile(screenshots_surf_i):
                            print("Using " + screenshots_surf_i + " as screenshot surface")
                        elif os.path.isfile(
                            os.path.join(argsDict["subjects_dir"], subject, "surf", screenshots_surf_i)
                        ):
                            screenshots_surf_i = os.path.join(
                                argsDict["subjects_dir"], subject, "surf", screenshots_surf_i
                            )
                            print("Using " + screenshots_surf_i + " as screenshot surface")
                        else:
                            print("\nERROR: cannot find the screenshots surface file " + screenshots_surf_i + "\n")
                            sys.exit(1)
                        screenshots_surf_subj.append(screenshots_surf_i)
                else:
                    screenshots_surf_subj = None

                # process
                createScreenshots(
                    SUBJECT=subject,
                    SUBJECTS_DIR=argsDict["subjects_dir"],
                    OUTFILE=outfile,
                    INTERACTIVE=False,
                    BASE=screenshots_base_subj,
                    OVERLAY=screenshots_overlay_subj,
                    SURF=screenshots_surf_subj,
                    VIEWS=argsDict["screenshots_views"],
                    LAYOUT=argsDict["screenshots_layout"],
                    ORIENTATION=argsDict["screenshots_orientation"],
                )

                # return
                screenshots_ok = True

            #
            except Exception as e:
                print("ERROR: screenshots module failed for subject " + subject)
                print("Reason: " + str(e))
                screenshots_ok = False

            # store data
            if screenshots_ok:
                imagesScreenshotsDict[subject] = outfile
            else:
                imagesScreenshotsDict[subject] = []

            # store data
            statusDict[subject].update({"screenshots": screenshots_ok})

        # ----------------------------------------------------------------------
        # run optional modules: surface plots

        if argsDict["surfaces"] is True or argsDict["surfaces_html"] is True:
            #
            try:
                # message
                print("-----------------------------")
                print("Creating surface plots ...")
                print("")

                # check / create subject-specific surfaces_outdir
                surfaces_outdir = os.path.join(argsDict["output_dir"], "surfaces", subject)
                if not os.path.isdir(surfaces_outdir):
                    os.makedirs(surfaces_outdir)

                # process
                createSurfacePlots(
                    SUBJECT=subject,
                    SUBJECTS_DIR=argsDict["subjects_dir"],
                    SURFACES_OUTDIR=surfaces_outdir,
                    VIEWS=argsDict["surfaces_views"],
                )
                # return
                surfaces_ok = True

            #
            except Exception as e:
                print("ERROR: surfaces module failed for subject " + subject)
                print("Reason: " + str(e))
                surfaces_ok = False

            # store data
            if surfaces_ok:
                imagesSurfacesDict[subject] = surfaces_outdir
            else:
                imagesSurfacesDict[subject] = []

            # store data
            statusDict[subject].update({"surfaces": surfaces_ok})

        # ----------------------------------------------------------------------
        # run optional modules: skullstrip

        if argsDict["skullstrip"] is True or argsDict["skullstrip_html"] is True:
            #
            try:
                # message
                print("-----------------------------")
                print("Creating skullstrip evaluation  ...")
                print("")

                # check / create subject-specific skullstrip_outdir
                skullstrip_outdir = os.path.join(argsDict["output_dir"], "skullstrip", subject)
                if not os.path.isdir(skullstrip_outdir):
                    os.makedirs(skullstrip_outdir)
                outfile = os.path.join(skullstrip_outdir, subject + ".png")

                # re-initialize
                skullstrip_base_subj = list()
                skullstrip_overlay_subj = list()
                skullstrip_surf_subj = list()

                # check skullstrip_base
                if os.path.isfile(os.path.join(argsDict["subjects_dir"], subject, "mri", "orig.mgz")):
                    skullstrip_base_subj = [os.path.join(argsDict["subjects_dir"], subject, "mri", "orig.mgz")]
                    print("Using " + "orig.mgz" + " as skullstrip base image")
                else:
                    print("\nERROR: cannot find the skullstrip base file " + "orig.mgz" + "\n")
                    sys.exit(1)

                # check skullstrip_overlay
                if os.path.isfile(os.path.join(argsDict["subjects_dir"], subject, "mri", "brainmask.mgz")):
                    skullstrip_overlay_subj = [os.path.join(argsDict["subjects_dir"], subject, "mri", "brainmask.mgz")]
                    print("Using " + "brainmask.mgz" + " as skullstrip overlay image")
                else:
                    print("\nERROR: cannot find the skullstrip overlay file " + "brainmask.mgz" + "\n")
                    sys.exit(1)

                # process
                createScreenshots(
                    SUBJECT=subject,
                    SUBJECTS_DIR=argsDict["subjects_dir"],
                    OUTFILE=outfile,
                    INTERACTIVE=False,
                    BASE=skullstrip_base_subj,
                    OVERLAY=skullstrip_overlay_subj,
                    SURF=None,
                    VIEWS=argsDict["screenshots_views"],
                    LAYOUT=argsDict["screenshots_layout"],
                    BINARIZE=True,
                    ORIENTATION=argsDict["screenshots_orientation"],
                )

                # return
                skullstrip_ok = True

            #
            except Exception as e:
                print("ERROR: skullstrip module failed for subject " + subject)
                print("Reason: " + str(e))
                skullstrip_ok = False

            # store data
            if skullstrip_ok:
                imagesSkullstripDict[subject] = outfile
            else:
                imagesSkullstripDict[subject] = []

            # store data
            statusDict[subject].update({"skullstrip": skullstrip_ok})

        # ----------------------------------------------------------------------
        # run optional modules: fornix

        if argsDict["fornix"] is True or argsDict["fornix_html"] is True:
            #
            try:
                # message
                print("-----------------------------")
                print("Checking fornix segmentation ...")
                print("")

                # check / create subject-specific fornix_outdir
                fornix_outdir = os.path.join(argsDict["output_dir"], "fornix", subject)
                if not os.path.isdir(fornix_outdir):
                    os.makedirs(fornix_outdir)
                fornix_screenshot_outfile = os.path.join(fornix_outdir, "cc.png")

                # process
                fornixShapeOutput = evaluateFornixSegmentation(
                    SUBJECT=subject,
                    SUBJECTS_DIR=argsDict["subjects_dir"],
                    OUTPUT_DIR=fornix_outdir,
                    CREATE_SCREENSHOT=FORNIX_SCREENSHOT,
                    SCREENSHOTS_OUTFILE=fornix_screenshot_outfile,
                    RUN_SHAPEDNA=FORNIX_SHAPE,
                    N_EIGEN=FORNIX_N_EIGEN,
                )

                # create a dictionary from fornix shape ouput
                fornixShapeDict = {
                    subject: dict(zip(map("fornixShapeEV{:0>3}".format, range(FORNIX_N_EIGEN)), fornixShapeOutput))
                }

                # return
                fornix_ok = True

            #
            except:
                fornixShapeDict = {
                    subject: dict(
                        zip(map("fornixShapeEV{:0>3}".format, range(FORNIX_N_EIGEN)), np.full(FORNIX_N_EIGEN, np.nan))
                    )
                }
                print("ERROR: fornix module failed for subject " + subject)
                fornix_ok = False

            # store data
            if FORNIX_SHAPE:
                metricsDict[subject].update(fornixShapeDict[subject])

            # store data
            if FORNIX_SCREENSHOT and fornix_ok:
                imagesFornixDict[subject] = fornix_screenshot_outfile
            else:
                imagesFornixDict[subject] = []

            # store data
            statusDict[subject].update({"fornix": fornix_ok})

        # ----------------------------------------------------------------------
        # run optional modules: hypothalamus

        if argsDict["hypothalamus"] is True or argsDict["hypothalamus_html"] is True:
            #
            try:
                # message
                print("-----------------------------")
                print("Checking hypothalamus segmentation ...")
                print("")

                # check / create subject-specific hypothalamus_outdir
                hypothalamus_outdir = os.path.join(argsDict["output_dir"], "hypothalamus", subject)
                if not os.path.isdir(hypothalamus_outdir):
                    os.makedirs(hypothalamus_outdir)
                hypothalamus_screenshot_outfile = os.path.join(hypothalamus_outdir, "hypothalamus.png")

                # process
                evaluateHypothalamicSegmentation(
                    SUBJECT=subject,
                    SUBJECTS_DIR=argsDict["subjects_dir"],
                    OUTPUT_DIR=hypothalamus_outdir,
                    CREATE_SCREENSHOT=HYPOTHALAMUS_SCREENSHOT,
                    SCREENSHOTS_OUTFILE=hypothalamus_screenshot_outfile,
                    SCREENSHOTS_ORIENTATION=argsDict["screenshots_orientation"],
                )

                # return
                hypothalamus_ok = True

            #
            except:
                print("ERROR: hypothalamus module failed for subject " + subject)
                hypothalamus_ok = False

            # store data
            if HYPOTHALAMUS_SCREENSHOT and hypothalamus_ok:
                imagesHypothalamusDict[subject] = hypothalamus_screenshot_outfile
            else:
                imagesHypothalamusDict[subject] = []

            # store data
            statusDict[subject].update({"hypothalamus": hypothalamus_ok})

        # ----------------------------------------------------------------------
        # run optional modules: hippocampus

        if argsDict["hippocampus"] is True or argsDict["hippocampus_html"] is True:
            #
            try:
                # message
                print("-----------------------------")
                print("Checking hippocampus segmentation ...")
                print("")

                # check / create subject-specific hippocampus_outdir
                hippocampus_outdir = os.path.join(argsDict["output_dir"], "hippocampus", subject)
                if not os.path.isdir(hippocampus_outdir):
                    os.makedirs(hippocampus_outdir)
                hippocampus_screenshot_outfile_left = os.path.join(hippocampus_outdir, "hippocampus-left.png")
                hippocampus_screenshot_outfile_right = os.path.join(hippocampus_outdir, "hippocampus-right.png")

                # process left
                evaluateHippocampalSegmentation(
                    SUBJECT=subject,
                    SUBJECTS_DIR=argsDict["subjects_dir"],
                    OUTPUT_DIR=hippocampus_outdir,
                    CREATE_SCREENSHOT=HIPPOCAMPUS_SCREENSHOT,
                    SCREENSHOTS_OUTFILE=hippocampus_screenshot_outfile_left,
                    SCREENSHOTS_ORIENTATION=argsDict["screenshots_orientation"],
                    HEMI="lh",
                    LABEL=argsDict["hippocampus_label"],
                )
                evaluateHippocampalSegmentation(
                    SUBJECT=subject,
                    SUBJECTS_DIR=argsDict["subjects_dir"],
                    OUTPUT_DIR=hippocampus_outdir,
                    CREATE_SCREENSHOT=HIPPOCAMPUS_SCREENSHOT,
                    SCREENSHOTS_OUTFILE=hippocampus_screenshot_outfile_right,
                    SCREENSHOTS_ORIENTATION=argsDict["screenshots_orientation"],
                    HEMI="rh",
                    LABEL=argsDict["hippocampus_label"],
                )

                # return
                hippocampus_ok = True

            #
            except:
                print("ERROR: hippocampus module failed for subject " + subject)
                hippocampus_ok = False

            # store data
            if HIPPOCAMPUS_SCREENSHOT and hippocampus_ok:
                imagesHippocampusLeftDict[subject] = hippocampus_screenshot_outfile_left
                imagesHippocampusRightDict[subject] = hippocampus_screenshot_outfile_right
            else:
                imagesHippocampusLeftDict[subject] = []
                imagesHippocampusRightDict[subject] = []

            # store data
            statusDict[subject].update({"hippocampus": hippocampus_ok})

        # --------------------------------------------------------------------------
        # message
        print("Finished subject", subject, "at", time.strftime("%Y-%m-%d %H:%M %Z", time.localtime(time.time())))
        print("")

    # --------------------------------------------------------------------------
    # run optional modules: outlier detection

    if argsDict["outlier"] is True:
        #
        try:
            # message
            print("---------------------------------------")
            print("Running outlier detection module ...")
            print("")

            # determine outlier-table and get data
            if argsDict["outlier_table"] is None:
                outlierDict = outlierTable()
            else:
                outlierDict = dict()
                with open(argsDict["outlier_table"], newline="") as csvfile:
                    outlierCsv = csv.DictReader(csvfile, delimiter=",")
                    for row in outlierCsv:
                        outlierDict.update({row["label"]: {"lower": float(row["lower"]), "upper": float(row["upper"])}})

            # process
            outlier_outdir = os.path.join(argsDict["output_dir"], "outliers")
            n_outlier_sample_nonpar, n_outlier_sample_param, n_outlier_norms = outlierDetection(
                argsDict["subjects"],
                argsDict["subjects_dir"],
                outlier_outdir,
                outlierDict,
                min_no_subjects=OUTLIER_N_MIN,
                hypothalamus=argsDict["hypothalamus"],
                hippocampus=argsDict["hippocampus"],
                hippocampus_label=argsDict["hippocampus_label"],
            )

            # create a dictionary from outlier module ouput
            outlierDict = dict()
            for subject in argsDict["subjects"]:
                outlierDict.update(
                    {
                        subject: {
                            "n_outlier_sample_nonpar": n_outlier_sample_nonpar[subject],
                            "n_outlier_sample_param": n_outlier_sample_param[subject],
                            "n_outlier_norms": n_outlier_norms[subject],
                        }
                    }
                )

            # return
            outlier_ok = True

        #
        except:
            # create a dictionary from outlier module ouput
            outlierDict = dict()
            for subject in subjects:
                outlierDict.update(
                    {
                        subject: {
                            "n_outlier_sample_nonpar": np.nan,
                            "n_outlier_sample_param": np.nan,
                            "n_outlier_norms": np.nan,
                        }
                    }
                )

            print("ERROR: outlier module failed")
            outlier_ok = False

        # store data
        for subject in argsDict["subjects"]:
            metricsDict[subject].update(outlierDict[subject])

        # message
        print("Done")
        print("")

    # --------------------------------------------------------------------------
    # generate output

    metricsFieldnames = ["subject"]

    # we pre-specify the fieldnames because we want to have this particular order
    metricsFieldnames.extend(
        [
            "wm_snr_orig",
            "gm_snr_orig",
            "wm_snr_norm",
            "gm_snr_norm",
            "cc_size",
            "holes_lh",
            "holes_rh",
            "defects_lh",
            "defects_rh",
            "topo_lh",
            "topo_rh",
            "con_snr_lh",
            "con_snr_rh",
            "rot_tal_x",
            "rot_tal_y",
            "rot_tal_z",
        ]
    )

    # collect other keys; need to iterate over subjects, because not all of them
    # necessarily have the same set of keys
    if argsDict["shape"] is True:
        shapeKeys = list()
        for subject in distDict.keys():
            if len(distDict[subject]) > 0:
                shapeKeys = list(np.unique(shapeKeys + list(distDict[subject].keys())))
        metricsFieldnames.extend(shapeKeys)

    if (argsDict["fornix"] is True or argsDict["fornix_html"] is True) and FORNIX_SHAPE is True:
        fornixKeys = list()
        for subject in fornixShapeDict.keys():
            if len(fornixShapeDict[subject]) > 0:
                fornixKeys = list(np.unique(fornixKeys + list(fornixShapeDict[subject].keys())))
        metricsFieldnames.extend(sorted(fornixKeys))

    if argsDict["outlier"] is True:
        outlierKeys = list()
        for subject in outlierDict.keys():
            if len(outlierDict[subject]) > 0:
                outlierKeys = list(np.unique(outlierKeys + list(outlierDict[subject].keys())))
        metricsFieldnames.extend(sorted(outlierKeys))

    # determine output file names
    path_data_file = os.path.join(argsDict["output_dir"], "qatools-results.csv")
    path_html_file = os.path.join(argsDict["output_dir"], "qatools-results.html")

    # write csv
    with open(path_data_file, "w") as datafile:
        csvwriter = csv.DictWriter(
            datafile, fieldnames=metricsFieldnames, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        csvwriter.writeheader()
        for subject in sorted(list(metricsDict.keys())):
            csvwriter.writerow(metricsDict[subject])

    # generate html output
    if (
        (argsDict["screenshots_html"] is True)
        or (argsDict["surfaces_html"] is True)
        or (argsDict["skullstrip_html"] is True)
        or (argsDict["fornix_html"] is True)
        or (argsDict["hypothalamus_html"] is True)
        or (argsDict["hippocampus_html"] is True)
    ):
        with open(path_html_file, "w") as htmlfile:
            print("<html>", file=htmlfile)
            print("<head>", file=htmlfile)
            print("<title>fsqc screenshots</title>", file=htmlfile)
            print("</head>", file=htmlfile)
            print(
                "<style> body, h1, h2, h3, h4, h5, h6  { font-family: Arial, Helvetica, sans-serif ; } </style>)",
                file=htmlfile,
            )
            print('<body style="background-color:Black">', file=htmlfile)

            # screenshots
            if argsDict["screenshots_html"] is True:
                print('<h1 style="color:white">Screenshots</h1>', file=htmlfile)
                for subject in sorted(list(imagesScreenshotsDict.keys())):
                    print('<h2 style="color:white">Subject ' + subject + "</h2>", file=htmlfile)
                    if imagesScreenshotsDict[subject]:  # should be False for empty string or empty list
                        if os.path.isfile(
                            os.path.join(
                                argsDict["output_dir"],
                                "screenshots",
                                subject,
                                os.path.basename(imagesScreenshotsDict[subject]),
                            )
                        ):
                            print(
                                '<p><a href="'
                                + os.path.join("screenshots", subject, os.path.basename(imagesScreenshotsDict[subject]))
                                + '">'
                                + '<img src="'
                                + os.path.join("screenshots", subject, os.path.basename(imagesScreenshotsDict[subject]))
                                + '" '
                                + 'alt="Image for subject '
                                + subject
                                + '" style="width:75vw;min_width:200px;"></img></a></p>',
                                file=htmlfile,
                            )

            # skullstrip
            if argsDict["skullstrip_html"] is True:
                print('<h1 style="color:white">Skullstrip</h1>', file=htmlfile)
                for subject in sorted(list(imagesSkullstripDict.keys())):
                    print('<h2 style="color:white">Subject ' + subject + "</h2>", file=htmlfile)
                    if imagesSkullstripDict[subject]:  # should be False for empty string or empty list
                        if os.path.isfile(
                            os.path.join(
                                argsDict["output_dir"],
                                "skullstrip",
                                subject,
                                os.path.basename(imagesSkullstripDict[subject]),
                            )
                        ):
                            print(
                                '<p><a href="'
                                + os.path.join("skullstrip", subject, os.path.basename(imagesSkullstripDict[subject]))
                                + '">'
                                + '<img src="'
                                + os.path.join("skullstrip", subject, os.path.basename(imagesSkullstripDict[subject]))
                                + '" '
                                + 'alt="Image for subject '
                                + subject
                                + '" style="width:75vw;min_width:200px;"></img></a></p>',
                                file=htmlfile,
                            )

            # surfaces
            if argsDict["surfaces_html"] is True:
                print('<h1 style="color:white">Surfaces</h1>', file=htmlfile)
                for subject in sorted(list(imagesSurfacesDict.keys())):
                    print('<h2 style="color:white">Subject ' + subject + "</h2>", file=htmlfile)
                    if imagesSurfacesDict[subject]:  # should be False for empty string or empty list
                        # Produce first all plots for pial then for inflated surface.
                        # Each view contains a left and right hemispheric plot.
                        _views_per_row = 2

                        from PIL import Image

                        filepath = os.path.join(
                            argsDict["output_dir"], "surfaces", subject, f'lh.pial.{argsDict["surfaces_views"][0]}.png'
                        )
                        img = Image.open(filepath)
                        width, height = img.size
                        width *= 2 * _views_per_row + 0.1

                        print("<p>", file=htmlfile)
                        print(f'<div style="width:{width}; background-color:black; ">', file=htmlfile)
                        print("<p>", file=htmlfile)
                        for i, v in enumerate(argsDict["surfaces_views"], start=1):
                            if os.path.isfile(
                                os.path.join(argsDict["output_dir"], "surfaces", subject, f"lh.pial.{v}.png")
                            ):
                                print(
                                    '<a href="'
                                    + os.path.join("surfaces", subject, f"lh.pial.{v}.png")
                                    + '">'
                                    + '<img src="'
                                    + os.path.join("surfaces", subject, f"lh.pial.{v}.png")
                                    + '" '
                                    + 'alt="Image for subject '
                                    + subject
                                    + '" style=""></img></a>',
                                    file=htmlfile,
                                )
                            if os.path.isfile(
                                os.path.join(argsDict["output_dir"], "surfaces", subject, f"rh.pial.{v}.png")
                            ):
                                print(
                                    '<a href="'
                                    + os.path.join("surfaces", subject, f"rh.pial.{v}.png")
                                    + '">'
                                    + '<img src="'
                                    + os.path.join("surfaces", subject, f"rh.pial.{v}.png")
                                    + '" '
                                    + 'alt="Image for subject '
                                    + subject
                                    + '" style=""></img></a>',
                                    file=htmlfile,
                                )
                            if i % _views_per_row == 0:
                                print("</p> <p>", file=htmlfile)
                        print("</p> <p>", file=htmlfile)
                        for i, v in enumerate(argsDict["surfaces_views"], start=1):
                            if os.path.isfile(
                                os.path.join(argsDict["output_dir"], "surfaces", subject, f"lh.inflated.{v}.png")
                            ):
                                print(
                                    '<a href="'
                                    + os.path.join("surfaces", subject, f"lh.inflated.{v}.png")
                                    + '">'
                                    + '<img src="'
                                    + os.path.join("surfaces", subject, f"lh.inflated.{v}.png")
                                    + '" '
                                    + 'alt="Image for subject '
                                    + subject
                                    + '" style=""></img></a>',
                                    file=htmlfile,
                                )
                            if os.path.isfile(
                                os.path.join(argsDict["output_dir"], "surfaces", subject, f"rh.inflated.{v}.png")
                            ):
                                print(
                                    '<a href="'
                                    + os.path.join("surfaces", subject, f"rh.inflated.{v}.png")
                                    + '">'
                                    + '<img src="'
                                    + os.path.join("surfaces", subject, f"rh.inflated.{v}.png")
                                    + '" '
                                    + 'alt="Image for subject '
                                    + subject
                                    + '" style=""></img></a>',
                                    file=htmlfile,
                                )
                            if i % _views_per_row == 0:
                                print("</p> <p>", file=htmlfile)
                        print("</p>", file=htmlfile)
                        print("</div>", file=htmlfile)
                        print("</p>", file=htmlfile)

            # fornix
            if argsDict["fornix_html"] is True:
                print('<h1 style="color:white">Fornix</h1>', file=htmlfile)
                for subject in sorted(list(imagesFornixDict.keys())):
                    print('<h2 style="color:white">Subject ' + subject + "</h2>", file=htmlfile)
                    if imagesFornixDict[subject]:  # should be False for empty string or empty list
                        if os.path.isfile(
                            os.path.join(
                                argsDict["output_dir"], "fornix", subject, os.path.basename(imagesFornixDict[subject])
                            )
                        ):
                            print(
                                '<p><a href="'
                                + os.path.join("fornix", subject, os.path.basename(imagesFornixDict[subject]))
                                + '">'
                                + '<img src="'
                                + os.path.join("fornix", subject, os.path.basename(imagesFornixDict[subject]))
                                + '" '
                                + 'alt="Image for subject '
                                + subject
                                + '" style="width:75vw;min_width:200px;"></img></a></p>',
                                file=htmlfile,
                            )

            # hypothalamus
            if argsDict["hypothalamus_html"] is True:
                print('<h1 style="color:white">Hypothalamus</h1>', file=htmlfile)
                for subject in sorted(list(imagesHypothalamusDict.keys())):
                    print('<h2 style="color:white">Subject ' + subject + "</h2>", file=htmlfile)
                    if imagesHypothalamusDict[subject]:  # should be False for empty string or empty list
                        if os.path.isfile(
                            os.path.join(
                                argsDict["output_dir"],
                                "hypothalamus",
                                subject,
                                os.path.basename(imagesHypothalamusDict[subject]),
                            )
                        ):
                            print(
                                '<p><a href="'
                                + os.path.join(
                                    "hypothalamus", subject, os.path.basename(imagesHypothalamusDict[subject])
                                )
                                + '">'
                                + '<img src="'
                                + os.path.join(
                                    "hypothalamus", subject, os.path.basename(imagesHypothalamusDict[subject])
                                )
                                + '" '
                                + 'alt="Image for subject '
                                + subject
                                + '" style="width:75vw;min_width:200px;"></img></a></p>',
                                file=htmlfile,
                            )

            # hippocampus
            if argsDict["hippocampus_html"] is True:
                print('<h1 style="color:white">hippocampus</h1>', file=htmlfile)
                for subject in sorted(list(imagesHippocampusLeftDict.keys())):
                    print('<h2 style="color:white">Subject ' + subject + "</h2>", file=htmlfile)
                    if imagesHippocampusLeftDict[subject]:  # should be False for empty string or empty list
                        if os.path.isfile(
                            os.path.join(
                                argsDict["output_dir"],
                                "hippocampus",
                                subject,
                                os.path.basename(imagesHippocampusLeftDict[subject]),
                            )
                        ):
                            print(
                                '<p><a href="'
                                + os.path.join(
                                    "hippocampus", subject, os.path.basename(imagesHippocampusLeftDict[subject])
                                )
                                + '">'
                                + '<img src="'
                                + os.path.join(
                                    "hippocampus", subject, os.path.basename(imagesHippocampusLeftDict[subject])
                                )
                                + '" '
                                + 'alt="Image for subject '
                                + subject
                                + '" style="width:75vw;min_width:200px;"></img></a></p>',
                                file=htmlfile,
                            )
                    if imagesHippocampusRightDict[subject]:  # should be False for empty string or empty list
                        if os.path.isfile(
                            os.path.join(
                                argsDict["output_dir"],
                                "hippocampus",
                                subject,
                                os.path.basename(imagesHippocampusRightDict[subject]),
                            )
                        ):
                            print(
                                '<p><a href="'
                                + os.path.join(
                                    "hippocampus", subject, os.path.basename(imagesHippocampusRightDict[subject])
                                )
                                + '">'
                                + '<img src="'
                                + os.path.join(
                                    "hippocampus", subject, os.path.basename(imagesHippocampusRightDict[subject])
                                )
                                + '" '
                                + 'alt="Image for subject '
                                + subject
                                + '" style="width:75vw;min_width:200px;"></img></a></p>',
                                file=htmlfile,
                            )

            #
            print("</body>", file=htmlfile)
            print("</html>", file=htmlfile)


# ------------------------------------------------------------------------------
# run qatools


def run_qatools(
    subjects_dir,
    output_dir,
    argsDict=None,
    subjects=None,
    subjects_file=None,
    shape=False,
    screenshots=False,
    screenshots_html=False,
    screenshots_base="default",
    screenshots_overlay="default",
    screenshots_surf="default",
    screenshots_views="default",
    screenshots_layout=None,
    screenshots_orientation="radiological",
    surfaces=False,
    surfaces_html=False,
    surfaces_views=["left", "right", "superior", "inferior"],
    skullstrip=False,
    skullstrip_html=False,
    fornix=False,
    fornix_html=False,
    hypothalamus=False,
    hypothalamus_html=False,
    hippocampus=False,
    hippocampus_html=False,
    hippocampus_label=None,
    outlier=False,
    outlier_table=None,
    fastsurfer=False,
):
    """
    a function to run the qatools submodules

    """

    # ------------------------------------------------------------------------------
    #

    #
    import sys

    # create argsDict
    if argsDict is None and (subjects_dir is None or output_dir is None):
        print(
            "\nERROR: nothing to do. Need to specify either the argsDict argument or the subjects_dir / output_dir arguments.\n"
        )
        sys.exit(1)

    elif argsDict is None and subjects_dir is not None and output_dir is not None:
        argsDict = dict()
        argsDict["subjects_dir"] = subjects_dir
        argsDict["output_dir"] = output_dir
        argsDict["subjects"] = subjects
        argsDict["subjects_file"] = subjects_file
        argsDict["shape"] = shape
        argsDict["screenshots"] = screenshots
        argsDict["screenshots_html"] = screenshots_html
        argsDict["screenshots_base"] = screenshots_base
        argsDict["screenshots_overlay"] = screenshots_overlay
        argsDict["screenshots_surf"] = screenshots_surf
        argsDict["screenshots_views"] = screenshots_views
        argsDict["screenshots_layout"] = screenshots_layout
        argsDict["screenshots_orientation"] = screenshots_orientation
        argsDict["surfaces"] = surfaces
        argsDict["surfaces_html"] = surfaces_html
        argsDict["surfaces_views"] = surfaces_views
        argsDict["skullstrip"] = skullstrip
        argsDict["skullstrip_html"] = skullstrip_html
        argsDict["fornix"] = fornix
        argsDict["fornix_html"] = fornix_html
        argsDict["hypothalamus"] = hypothalamus
        argsDict["hypothalamus_html"] = hypothalamus_html
        argsDict["hippocampus"] = hippocampus
        argsDict["hippocampus_html"] = hippocampus_html
        argsDict["hippocampus_label"] = hippocampus_label
        argsDict["outlier"] = outlier
        argsDict["outlier_table"] = outlier_table
        argsDict["fastsurfer"] = fastsurfer

    elif (argsDict is not None) and (subjects_dir is not None or output_dir is not None):
        print("\nERROR: cannot specify the argsDict and the subjects_dir / output_dir arguments at the same time.\n")
        sys.exit(1)

    # check arguments
    argsDict = _check_arguments(argsDict)

    # check packages
    _check_packages()

    # run qatools
    _do_qatools(argsDict)
