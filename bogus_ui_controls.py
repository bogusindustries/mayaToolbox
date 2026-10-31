import maya.cmds as cmds

class BogusUIControls:
    def __init__(self):
        print("BogusUIControls")

    def fixViewport(self):
        cmds.ogs(reset=True)
    
    def toggleInfoDisplay(self):
        cmds.TogglePolyCount()

    def toggleObjDetails(self):
        cmds.ToggleObjectDetails()
    
    def arrangeSingleWindow(self):
        cmds.SingleViewArrangement()

    def arrangeTwoWindows(self):
        cmds.TwoSideBySideViewArrangement()

    def arrangeTwoWindowsStacked(self):
        cmds.TwoStackedViewArrangement()

    def arrangeThreeWindowsTop(self):
        cmds.ThreeTopSplitViewArrangement()

    def arrangeThreeWindowsLeft(self):
        cmds.ThreeLeftSplitViewArrangement()

    def arrangeThreeWindowsBottom(self):
        cmds.ThreeBottomSplitViewArrangement()

    def arrangeThreeWindowsRight(self):
        cmds.ThreeRightSplitViewArrangement()

    def arrangeFourWindows(self):
        cmds.FourViewArrangement()