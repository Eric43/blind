# Basic todo list no particular order.

The blinding functions/package (loosely speaking) were designed for CLI use as needed.  The current set up is designed to be easier to package in docker (MacOS MBP in single architecture docker may not work)

### Current

1.  Finish the ocr_blind function and include **kwargs to allow for fine tuning of the readtext(), inpaint radius and fill color.  While fill color is really not needed it is nice to see the block during turning.
NOTE: Considered adding the ability to change inpaint between TELEA and NS but NS in the few test images was less drastic of a transition.
2.  Block blinding work to include working the use of more complex block shapes.  A header L could remove the majority of PHI with no use of the ai models saving costs and time.
3.  Considering depreciating the line method and replacing with the polyfill mask method.  Although this needs additional testing.
4.  General clean-up and testing needed.
5.  Add language blinding support (in progress)

### Future

1.  Migrate some of the video blinding CLI currently in use with Keras-OCR to easyOCR
2.  Optimize the ocr_blind function for many images without starting a new reader/session.  This was an issue for TF and unknown for pytorch.
3.  Finish integrating prior functions to work with pytorch backend.
4.  Some difference have been seen (anecdotal) between different institutions image sources and require different tuning settings.  Maybe nice to do an auto tune (SGD?) just playing with the readtext settings and images with known text box N.

### Docker

1.  Look into development of a multi-architecture basic docker for these functions.  MacOS MBP (MacOS equivalent of cudaDNN or RoCM for leveraging GPU for the underlying maths).  Works in VENV and works in Ubuntu Pytorch cudaDNN/Nvidia(tm) docker (Unknown build and version).
2.  If needed for MacOS development can research the Apple specific solution "Apple Containers." Open source but seems to lack some of the docker-compose functions.  Needs additional background research.

### Utils

1.  Needed to develop a random words on a US video background for OCR_blind of videos and later adding noise for S/N ratio testing.

Need to figure out why the codec is not saving correctly:

FPS:  15.0 / Frame count:  30 / Frame width:  640 / Frame height:  480
[mpeg4 @ 0x91f31df80] ac-tex damaged at 10 19
[mpeg4 @ 0x91f31df80] Error at MB: 789
/Users/ericolle/Documents/pytorch/blind/.venv/lib/python3.12/site-packages/torch/utils/data/dataloader.py:752: UserWarning: 'pin_memory' argument is set as true but not supported on MPS now, device pinned memory won't be used.
  super().__init__(loader)
The AI module has FAILED to blind the frame.
The video frame: 0 OF 30 failure

