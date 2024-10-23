# Hybrid Toolbox
# Compatible with Maya 2022.5
# Designed/Written by John Zilka
# Last edited 10-23-2024

try:
    from PySide2 import QtGui, QtWidgets, QtCore
    from shiboken2 import wrapInstance
except:
    from PySide6 import QtGui, QtWidgets, QtCore
    from shiboken6 import wrapInstance

import sys
from maya.OpenMayaUI import MQtUtil
import maya.cmds as cmds

class HybridToolboxGUI(QtWidgets.QMainWindow):
    def __init__(self, windowName, parent = None):
        super().__init__(parent)
        self.setObjectName(windowName)
        self.setMinimumWidth(790)

        # On macOS make window a Tool to keep it on top of Maya
        if sys.platform == "darwin":
            self.setWindowFlag(QtCore.Qt.Tool, True)

        # Variables
        self.deformersGroup = None
        self.groupType = None
        self.customColorChoice = 0
        self.useCustomColorChoice = False
        self.selectSearchCurrentChoice = False
        self.addToSelectionChoice = False
        self.objectCleanup = False

        self.jointAxisChoice = "X"
        self.jointNumberChoice = 10
        self.jointSpacingChoice = 1.0000
        self.jointOrientationChoice = "xyz"
        self.jointSecondaryChoice = "yup"

        self.transformsArray = []
        self.locatorsArray = []

        self.childArray = []
        self.parentConstraintArray = []
        self.pointConstraintArray = []
        self.scaleConstraintArray = []
        self.constrainedObjectArray = []
        self.constraintParent = None
        self.constraintArray = []
        self.AEParentConstraints = []
        self.AEScaleConstraints = []
        self.parentConstraintChoice = "parent"
        self.pointConstraintChoice = ""
        self.orientConstraintChoice = ""
        self.scaleConstraintChoice = ""
        self.maintainOffsetChoice = True
        self.allowMultipleConstraintsChoice = False
        self.constraintParents = set()
        self.constraintChildren = set()

        # Create window base
        self.toolboxBaseWindow = QtWidgets.QTabWidget()
        self.setWindowTitle(windowName)
        self.setCentralWidget(self.toolboxBaseWindow)

        self.uiToolsTab = QtWidgets.QWidget()
        self.creationToolsTab = QtWidgets.QWidget()
        self.selectionToolsTab = QtWidgets.QWidget()
        self.curveToolsTab = QtWidgets.QWidget()
        self.jointToolsTab = QtWidgets.QWidget()
        self.constraintToolsTab = QtWidgets.QWidget()
        self.sceneInfoTab = QtWidgets.QWidget()

        self.toolboxBaseWindow.addTab(self.uiToolsTab, "UI Tools")
        self.toolboxBaseWindow.addTab(self.creationToolsTab, "Creation Tools")
        self.toolboxBaseWindow.addTab(self.selectionToolsTab, "Selection Tools")
        self.toolboxBaseWindow.addTab(self.curveToolsTab, "Curve Tools")
        self.toolboxBaseWindow.addTab(self.jointToolsTab, "Joint Tools")
        self.toolboxBaseWindow.addTab(self.constraintToolsTab, "Constraint Tools")
        self.toolboxBaseWindow.addTab(self.sceneInfoTab, "Info")

        self.toolboxLayout = QtWidgets.QFormLayout()
        self.toolboxBaseWindow.setLayout(self.toolboxLayout)

        self.uiToolsCreateGUI()
        self.creationToolsCreateGUI()
        self.selectionToolsCreateGUI()
        self.curveToolsCreateGUI()
        self.jointToolsCreateGUI()
        self.constraintToolsCreateGUI()
        self.sceneInfoCreateGUI()
        self.getSceneInfo()

        self.show()
    # UI Tools GUI
    def uiToolsCreateGUI(self):
    # Widgets
        # update viewport 2.0 button
        self.fixViewportButton = QtWidgets.QPushButton("Fix Viewport")
        self.fixViewportButton.setStatusTip("Resets Viewport 2.0")
        self.fixViewportButton.setWhatsThis("Resets Viewport 2.0 in instances when scene is displayed incorrectly.")
        # Info display Buttons
        self.infoButton = QtWidgets.QPushButton("Toggle Info Display")
        self.detailsButton = QtWidgets.QPushButton("Toggle Object Details")
        # Window arrangement buttons
        self.singlePaneButton = QtWidgets.QPushButton("Single Pane")
        self.twoPaneSideButton = QtWidgets.QPushButton("Two Panes")
        self.twoPaneStackedButton = QtWidgets.QPushButton("Two Panes Stacked")
        self.threePaneSplitTopButton = QtWidgets.QPushButton("Three Panes Split Top")
        self.threePaneSplitLeftButton = QtWidgets.QPushButton("Three Panes Split Left")
        self.threePaneSplitBottomButton = QtWidgets.QPushButton("Three Panes Split Bottom")
        self.threePaneSplitRightButton = QtWidgets.QPushButton("Three Panes Split Right")
        self.fourPaneButton = QtWidgets.QPushButton("Four Panes")
    # Layouts
        self.fixViewportLayout = QtWidgets.QHBoxLayout()
        self.fixViewportLayout.addWidget(self.fixViewportButton)
        
        self.dispalyInfoLayout = QtWidgets.QHBoxLayout()
        self.dispalyInfoLayout.addWidget(self.infoButton)
        self.dispalyInfoLayout.addWidget(self.detailsButton)
        
        self.windowArrangementsLayout = QtWidgets.QGridLayout()
        self.windowArrangementsLayout.addWidget(self.singlePaneButton, 0, 0)
        self.windowArrangementsLayout.addWidget(self.twoPaneSideButton, 0, 1)
        self.windowArrangementsLayout.addWidget(self.twoPaneStackedButton, 0, 2)
        self.windowArrangementsLayout.addWidget(self.threePaneSplitTopButton, 0, 3)
        self.windowArrangementsLayout.addWidget(self.threePaneSplitLeftButton, 1, 0)
        self.windowArrangementsLayout.addWidget(self.threePaneSplitBottomButton, 1, 1)
        self.windowArrangementsLayout.addWidget(self.threePaneSplitRightButton, 1, 2)
        self.windowArrangementsLayout.addWidget(self.fourPaneButton, 1, 3)
        
        self.uiToolsMainLayout = QtWidgets.QFormLayout(self.uiToolsTab)
        self.uiToolsMainLayout.addRow("",self.fixViewportLayout)
        self.uiToolsMainLayout.addRow("",self.dispalyInfoLayout)
        self.uiToolsMainLayout.addRow("",self.windowArrangementsLayout)
    # Connections
        self.fixViewportButton.clicked.connect(lambda: self.fixViewport())
        self.infoButton.clicked.connect(lambda: self.toggleInfoDisplay())
        self.detailsButton.clicked.connect(lambda: self.toggleObjDetails())
        self.singlePaneButton.clicked.connect(lambda: self.arrangeSingleWindow())
        self.twoPaneSideButton.clicked.connect(lambda: self.arrangeTwoWindows())
        self.twoPaneStackedButton.clicked.connect(lambda: self.arrangeTwoWindowsStacked())
        self.threePaneSplitTopButton.clicked.connect(lambda: self.arrangeThreeWindowsTop())
        self.threePaneSplitLeftButton.clicked.connect(lambda: self.arrangeThreeWindowsLeft())
        self.threePaneSplitBottomButton.clicked.connect(lambda: self.arrangeThreeWindowsBottom())
        self.threePaneSplitRightButton.clicked.connect(lambda: self.arrangeThreeWindowsRight())
        self.fourPaneButton.clicked.connect(lambda: self.arrangeFourWindows())
    
    # Creation Tools GUI
    def creationToolsCreateGUI(self):
    # Widgets
        self.locatorAtVertsButton = QtWidgets.QPushButton("Locator at Verts")
        self.locatorAtVertsButton.setStatusTip("Create locator per selected vertex")
        self.locatorAtVertsButton.setWhatsThis("Creates a locator at each selected vertex. Locators are placed in \"VertexLocators_Grp\".")
        self.locatorAtCenterVertsButton = QtWidgets.QPushButton("Locator at Center Verts")
        self.locatorAtCenterVertsButton.setStatusTip("Create locator at center position of selected vertices.")
        self.locatorAtCenterVertsButton.setWhatsThis("Creates a locator at the center of selected vertices. Locator is placed in \"VertexLocators_Grp\".")
        self.globalControlButton = QtWidgets.QPushButton("Global Control")
        self.customControlButton = QtWidgets.QPushButton("Custom Control")
        self.customControlButton.setStatusTip("Create custom control from selected curves")
        self.customControlButton.setWhatsThis("Combines selected curves into 1 transform node and prepares them for use as an animation control object. Control placed in \"Controls_Grp\".")
        self.useCustomColorCheckBox = QtWidgets.QCheckBox("Use CustomColor")
        self.customColorDialog = QtWidgets.QLineEdit()
        self.customColorDialog.setReadOnly(True)
        self.customColorDialog.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.customColorDialog.setFixedWidth(50)
        self.customColorSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.customColorSlider.setTickInterval(1)
        self.customColorSlider.setMaximum(31)
        self.customColorSlider.setSliderPosition(17)
        self.setCustomColorButton = QtWidgets.QPushButton("Set Custom Color")
    
    # Layouts
        self.createLocatorsLayout = QtWidgets.QHBoxLayout()
        self.createLocatorsLayout.addWidget(self.locatorAtVertsButton)
        self.createLocatorsLayout.addWidget(self.locatorAtCenterVertsButton)

        self.createControlsLayout = QtWidgets.QHBoxLayout()
        self.createControlsLayout.addWidget(self.globalControlButton)
        self.createControlsLayout.addWidget(self.customControlButton)
        self.createControlsLayout.addWidget(self.useCustomColorCheckBox)
        self.createControlsLayout.addWidget(self.customColorDialog)
        self.createControlsLayout.addWidget(self.customColorSlider)
        self.createControlsLayout.addWidget(self.setCustomColorButton)

        self.creationToolsMainLayout = QtWidgets.QFormLayout(self.creationToolsTab)
        self.creationToolsMainLayout.addRow("", self.createLocatorsLayout)
        self.creationToolsMainLayout.addRow("", self.createControlsLayout)
    
    # Connections
        self.locatorAtVertsButton.clicked.connect(lambda: self.createLocatorsAtVerts())
        self.locatorAtCenterVertsButton.clicked.connect(lambda: self.locatorAtCenterVerts())
        self.globalControlButton.clicked.connect(lambda: self.createGlobalControl())
        self.customControlButton.clicked.connect(lambda: self.createCustomControl())
        self.useCustomColorCheckBox.stateChanged.connect(lambda: self.setUseCustomColor())
        self.customColorSlider.valueChanged.connect(lambda: self.setColorSlider())
        self.setCustomColorButton.clicked.connect(lambda: self.setCustomControlColor())
    
    # Selection Tools GUI
    def selectionToolsCreateGUI(self):
    # Widgets
        self.selectSearchCurrentCheckbox = QtWidgets.QCheckBox("Search Current Selection")
        self.selectSearchCurrentCheckbox.setChecked(False)
        self.selectSearchCurrentCheckbox.setStatusTip("When checked, selections are only applied to currently selected object and descendants.")
        self.selectAddToCheckbox = QtWidgets.QCheckBox("Add To Selection")
        self.selectAddToCheckbox.setStatusTip("Add to current selection.")
        self.selectAddToCheckbox.setWhatsThis("When checked, selections will be added to current selection.")
        
        # Hierarchy Selections
        self.selectionHierarchyLabel = QtWidgets.QLabel("Hierarchy Selections")
        self.selectHierarchyButton = QtWidgets.QPushButton("Select Hierarchy")
        self.findRootButton = QtWidgets.QPushButton("Select Root")
        self.findRootButton.setStatusTip("Selects root object.")
        self.findRootButton.setWhatsThis("Selects top-most parent object of current selection.")
        
        # Object Selections
        self.selectionTypesLabel = QtWidgets.QLabel("Object Selections")
        self.selectAllMeshesButton = QtWidgets.QPushButton("Select Polygons")
        self.selectAllNurbsButton = QtWidgets.QPushButton("Select Nurbs")
        self.selectAllCurvesButton = QtWidgets.QPushButton("Select Curves")
        self.selectAllJointsButton = QtWidgets.QPushButton("Select Joints")
        self.selectAllJointsButton.setStatusTip("Selects all root joints.")
        self.selectAllJointsButton.setWhatsThis("Selects every root joint in the scene.")
        self.selectAllLocatorsButton = QtWidgets.QPushButton("Select Locators")
        
        # Light Selections
        self.selectionLightsLabel = QtWidgets.QLabel("Light Selections")
        self.selectAllMayaLightsButton = QtWidgets.QPushButton("Select Maya Lights")
        self.selectAllRedshiftLightsButton = QtWidgets.QPushButton("Select Redshift Lights")
        self.selectAllVRayLightsButton = QtWidgets.QPushButton("Select VRay Lights")
        self.selectAllLightsButton = QtWidgets.QPushButton("Select All Lights")

        # Animation Selections
        self.selectAnimLabel = QtWidgets.QLabel("Animation Selections")
        self.selectAnimCurvesButton = QtWidgets.QPushButton("Select Anim Curves")
        self.selectAnimCurvesButton.setStatusTip("Selects Animation Curves.")
        self.selectAnimCurvesButton.setWhatsThis("Selects all animation curves in the scene.")
        self.selectAllConstraintsButton = QtWidgets.QPushButton("Select Constraints")
        self.selectAllIKHandlesButton = QtWidgets.QPushButton("Select IK Handles")
        self.selectBlendShapeMeshesButton = QtWidgets.QPushButton("Select BlendShape Meshes")

        self.selectFeedbackLabel = QtWidgets.QLabel("Number of objects :")
        self.selectFeedbackOutput = QtWidgets.QLabel("")

    # Layouts
        self.selectionColumnWidth = 115
        # Selection Options Layout
        self.selectionOptionsLayout = QtWidgets.QHBoxLayout()
        self.selectionOptionsLayout.addWidget(self.selectSearchCurrentCheckbox)
        self.selectionOptionsLayout.addWidget(self.selectAddToCheckbox)

        # Selection Hierarchy Layout
        self.selectionHierarchyLayout = QtWidgets.QGridLayout()
        self.selectionHierarchyLayout.setColumnMinimumWidth(0, self.selectionColumnWidth)
        self.selectionHierarchyLayout.setColumnMinimumWidth(1, self.selectionColumnWidth)
        self.selectionHierarchyLayout.addWidget(self.selectionHierarchyLabel, 0,0)
        self.selectionHierarchyLayout.addWidget(self.selectHierarchyButton, 1,0)
        self.selectionHierarchyLayout.addWidget(self.findRootButton, 1, 1)

        # Selection Object Types Layout
        self.selectionTypesLayout = QtWidgets.QGridLayout()
        self.selectionTypesLayout.setColumnMinimumWidth(0, self.selectionColumnWidth)
        self.selectionTypesLayout.setColumnMinimumWidth(1, self.selectionColumnWidth)
        self.selectionTypesLayout.setColumnMinimumWidth(2, self.selectionColumnWidth)
        self.selectionTypesLayout.setColumnMinimumWidth(3, self.selectionColumnWidth)
        self.selectionTypesLayout.setColumnMinimumWidth(4, self.selectionColumnWidth)
        self.selectionTypesLayout.setColumnMinimumWidth(5, self.selectionColumnWidth)
        self.selectionTypesLayout.addWidget(self.selectionTypesLabel, 0,0)
        self.selectionTypesLayout.addWidget(self.selectAllMeshesButton, 1, 0)
        self.selectionTypesLayout.addWidget(self.selectAllNurbsButton, 1, 1)
        self.selectionTypesLayout.addWidget(self.selectAllCurvesButton, 1, 2)
        self.selectionTypesLayout.addWidget(self.selectAllJointsButton, 1, 3)
        self.selectionTypesLayout.addWidget(self.selectAllLocatorsButton, 1, 4)
        
        # Selection Lights Layout
        self.selectionLightsLayout = QtWidgets.QGridLayout()
        self.selectionLightsLayout.setColumnMinimumWidth(0, self.selectionColumnWidth)
        self.selectionLightsLayout.setColumnMinimumWidth(1, self.selectionColumnWidth)
        self.selectionLightsLayout.setColumnMinimumWidth(2, self.selectionColumnWidth)
        self.selectionLightsLayout.setColumnMinimumWidth(3, self.selectionColumnWidth)
        self.selectionLightsLayout.addWidget(self.selectionLightsLabel, 0,0)
        self.selectionLightsLayout.addWidget(self.selectAllMayaLightsButton, 1,0)
        self.selectionLightsLayout.addWidget(self.selectAllRedshiftLightsButton, 1,1)
        self.selectionLightsLayout.addWidget(self.selectAllVRayLightsButton, 1,2)
        self.selectionLightsLayout.addWidget(self.selectAllLightsButton, 1,3)

        # Selection Animaion Layout
        self.selectionAnimationLayout = QtWidgets.QGridLayout()
        self.selectionAnimationLayout.setColumnMinimumWidth(0 ,self.selectionColumnWidth)
        self.selectionAnimationLayout.setColumnMinimumWidth(1 ,self.selectionColumnWidth)
        self.selectionAnimationLayout.setColumnMinimumWidth(2 ,self.selectionColumnWidth)
        self.selectionAnimationLayout.setColumnMinimumWidth(3 ,self.selectionColumnWidth)
        self.selectionAnimationLayout.setColumnMinimumWidth(4 ,self.selectionColumnWidth)
        self.selectionAnimationLayout.addWidget(self.selectAnimLabel, 0, 0)
        self.selectionAnimationLayout.addWidget(self.selectAnimCurvesButton, 1 ,0)
        self.selectionAnimationLayout.addWidget(self.selectAllConstraintsButton, 1, 1)
        self.selectionAnimationLayout.addWidget(self.selectAllIKHandlesButton, 1, 2)
        self.selectionAnimationLayout.addWidget(self.selectBlendShapeMeshesButton, 1, 3)

        # Selection Feedback Layout
        self.selectionFeedbackLayout = QtWidgets.QHBoxLayout()
        self.selectionFeedbackLayout.addWidget(self.selectFeedbackLabel)
        self.selectionFeedbackLayout.addWidget(self.selectFeedbackOutput)

        # Selection tools main layout
        self.selectionToolsMainLayout = QtWidgets.QFormLayout(self.selectionToolsTab)
        self.selectionToolsMainLayout.addRow("",self.selectionOptionsLayout)
        self.selectionToolsMainLayout.addRow("",self.selectionHierarchyLayout)
        self.selectionToolsMainLayout.addRow("",self.selectionTypesLayout)
        self.selectionToolsMainLayout.addRow("",self.selectionLightsLayout)
        self.selectionToolsMainLayout.addRow("",self.selectionAnimationLayout)
        self.selectionToolsMainLayout.addRow("",self.selectionFeedbackLayout)

    # Connections
        self.selectSearchCurrentCheckbox.stateChanged.connect(lambda: self.getSearchCurrent())
        self.selectAddToCheckbox.stateChanged.connect(lambda: self.getAddToSelection())
        self.selectHierarchyButton.clicked.connect(lambda: self.selectHierarchy())
        self.findRootButton.clicked.connect(lambda: self.findRoot())
        self.selectAllMeshesButton.clicked.connect(lambda: self.selectAllMeshes())
        self.selectAllNurbsButton.clicked.connect(lambda: self.selectAllNurbsSurfaces())
        self.selectAllCurvesButton.clicked.connect(lambda: self.selectAllCurves())
        self.selectAllJointsButton.clicked.connect(lambda: self.selectAllJointRoots())
        self.selectAllLocatorsButton.clicked.connect(lambda: self.selectAllLocators())
        self.selectAllMayaLightsButton.clicked.connect(lambda: self.selectAllMayaLights())
        self.selectAllRedshiftLightsButton.clicked.connect(lambda: self.selectAllRedshiftLights())
        self.selectAllVRayLightsButton.clicked.connect(lambda: self.selectAllVRayLights())
        self.selectAllLightsButton.clicked.connect(lambda: self.selectAllLights())
        self.selectAnimCurvesButton.clicked.connect(lambda: self.selectAnimationCurves())
        self.selectAllConstraintsButton.clicked.connect(lambda: self.selectAllConstraints())
        self.selectAllIKHandlesButton.clicked.connect(lambda: self.selectAllIKHandles())
        self.selectBlendShapeMeshesButton.clicked.connect(lambda: self.selectBlendshapeMeshes())
    
    # Curve Tools GUI
    def curveToolsCreateGUI(self):
    # Widgets
        self.curveAtObjectsButton = QtWidgets.QPushButton("Curve at Objects")
        self.curveAtObjectsButton.setStatusTip("Creates a curve with a CV at each selected object")
        self.curveAtObjectsButton.setWhatsThis("Creates a curve with a CV at each selected object. Minimun of 4 objects required. Curve placed in \"Curves_Grp\".")
        self.cleanupObjectsCheckbox = QtWidgets.QCheckBox("Cleanup Objects")
        self.cleanupObjectsCheckbox.setStatusTip("Delete objects after creating")
        self.cleanupObjectsCheckbox.setWhatsThis("When checked, objects used to create the curve will be deleted immediately.")
        self.clusterAtCVsButton = QtWidgets.QPushButton("Cluster at CVs")
        self.clusterAtCVsButton.setStatusTip("Creates a cluster at each CV of selected curve")
        self.clusterAtCVsButton.setWhatsThis("Creates a cluster at each CV of selected curve. Clusters placed in \"Clusters_Grp\".")
    # Layouts
        # Curve at selection layout
        self.curveAtObjectsLayout = QtWidgets.QHBoxLayout()
        self.curveAtObjectsLayout.addWidget(self.curveAtObjectsButton)
        self.curveAtObjectsLayout.addWidget(self.cleanupObjectsCheckbox)

        # Cluster at CVs layout
        self.clusterAtCVsLayout = QtWidgets.QHBoxLayout()
        self.clusterAtCVsLayout.addWidget(self.clusterAtCVsButton)

        # Create Curve tools main layout and connect sub layouts
        self.curveToolsMainLayout = QtWidgets.QFormLayout(self.curveToolsTab)
        self.curveToolsMainLayout.addRow("", self.curveAtObjectsLayout)
        self.curveToolsMainLayout.addRow("", self.clusterAtCVsLayout)
    # Connections
        self.curveAtObjectsButton.clicked.connect(lambda: self.createCurveAtObjects())
        self.cleanupObjectsCheckbox.stateChanged.connect(lambda:self.setCurveObjectCleanup())
        self.clusterAtCVsButton.clicked.connect(lambda: self.clusterAtCV())
    
    # Joint Tools GUI
    def jointToolsCreateGUI(self):
    #Widgets
        # Select joint hierarchy
        self.jointHierarchyButton = QtWidgets.QPushButton("Select Joint Hierarchy")
        # Create Joints at
        self.jointAtCVsButton = QtWidgets.QPushButton("Joints at CVs")
        self.jointAtObjectsButton = QtWidgets.QPushButton("Joints at Objects")
        # Joint axis
        column1_fixedWidth = 100
        column2_fixedWidth = 100
        self.jointCreationAxisLabel = QtWidgets.QLabel("Creation Axis")
        self.jointCreationAxisLabel.setFixedWidth(column1_fixedWidth)
        self.jointAxisSelector = QtWidgets.QComboBox()
        self.jointAxisSelector.addItems([
            "X",
            "-X",
            "Y",
            "-Y",
            "Z",
            "-Z",
        ])
        self.jointAxisSelectorIndex = self.jointAxisSelector.currentIndex()
        self.jointAxisSelector.setFixedWidth(column2_fixedWidth)
        # Joint number
        self.jointNumber = 10
        self.jointNumberLabel = QtWidgets.QLabel("Number of Joints")
        self.jointNumberLabel.setFixedWidth(column1_fixedWidth)
        self.jointNumberInput = QtWidgets.QLineEdit()
        self.jointNumberInput.setText("10")
        self.jointNumberInput.setFixedWidth(column2_fixedWidth)
        intValidator = QtGui.QIntValidator()
        self.jointNumberInput.setValidator(intValidator)
        # Joint spacing
        self.jointSpacing = 1.0000
        self.jointSpacingLabel = QtWidgets.QLabel("Joint Spacing")
        self.jointSpacingLabel.setFixedWidth(column1_fixedWidth)
        self.jointSpacingInput = QtWidgets.QLineEdit()
        self.jointSpacingInput.setText("1.0000")
        self.jointSpacingInput.setFixedWidth(column2_fixedWidth)
        floatValidator = QtGui.QDoubleValidator()
        floatValidator.setDecimals(4)
        floatValidator.setBottom(0.0001)
        self.jointSpacingInput.setValidator(floatValidator)
        # Joint Orientation
        self.jointOrientationLabel = QtWidgets.QLabel("Orientation Axis")
        self.jointOrientationLabel.setFixedWidth(column1_fixedWidth)
        self.jointOrientationSelector = QtWidgets.QComboBox()
        self.jointOrientationSelector.addItems([
            "xyz",
            "yzx",
            "zxy",
            "zyx",
            "yxz",
            "xzy",
            "none"
        ])
        self.jointOrientationSelectorIndex = self.jointOrientationSelector.currentIndex()
        self.jointOrientationSelector.setFixedWidth(column2_fixedWidth)
        # Secondary Axis
        self.jointSecondaryLabel = QtWidgets.QLabel("Secondary Axis")
        self.jointSecondaryLabel.setFixedWidth(column1_fixedWidth)
        self.jointSecondarySelector = QtWidgets.QComboBox()
        self.jointSecondarySelector.addItems([
            "xup",
            "xdown",
            "yup",
            "ydown",
            "zup",
            "zdown",
        ])
        self.jointSecondarySelector.setFixedWidth(column2_fixedWidth)
        self.jointSecondarySelector.setCurrentIndex(2)
        self.jointSecondarySelectorIndex = self.jointSecondarySelector.currentIndex()
        # Create/Reset
        self.jointCreateChainButton = QtWidgets.QPushButton("Create Joint Chain")
        self.jointCreateChainButton.setFixedWidth(column1_fixedWidth)
        self.jointResetButton = QtWidgets.QPushButton("Reset")
        self.jointResetButton.setFixedWidth(column2_fixedWidth)
    # Layouts
        # Joint hierarchy selection layout
        self.jointSelectionLayout = QtWidgets.QHBoxLayout()
        self.jointSelectionLayout.addWidget(self.jointHierarchyButton)
        # Create joints at CVs or objects layout
        self.jointCreateAtLayout = QtWidgets.QHBoxLayout()
        self.jointCreateAtLayout.addWidget(self.jointAtCVsButton)
        self.jointCreateAtLayout.addWidget(self.jointAtObjectsButton)
        # Joint create chain layout
        self.jointCreateChainLayout = QtWidgets.QGridLayout()
        self.jointCreateChainLayout.addWidget(self.jointCreationAxisLabel, 0,0)
        self.jointCreateChainLayout.addWidget(self.jointAxisSelector, 0,1)
        self.jointCreateChainLayout.addWidget(self.jointNumberLabel, 1,0)
        self.jointCreateChainLayout.addWidget(self.jointNumberInput, 1,1)
        self.jointCreateChainLayout.addWidget(self.jointSpacingLabel, 2,0)
        self.jointCreateChainLayout.addWidget(self.jointSpacingInput, 2,1)
        self.jointCreateChainLayout.addWidget(self.jointOrientationLabel, 3,0)
        self.jointCreateChainLayout.addWidget(self.jointOrientationSelector, 3,1)
        self.jointCreateChainLayout.addWidget(self.jointSecondaryLabel, 4,0)
        self.jointCreateChainLayout.addWidget(self.jointSecondarySelector, 4,1)
        self.jointCreateChainLayout.addWidget(self.jointCreateChainButton, 5,0)
        self.jointCreateChainLayout.addWidget(self.jointResetButton, 5,1)
        
        # Main joint tools layout and connections
        self.jointToolsMainLayout = QtWidgets.QFormLayout(self.jointToolsTab)
        self.jointToolsMainLayout.addRow("", self.jointSelectionLayout)
        self.jointToolsMainLayout.addRow("", self.jointCreateAtLayout)
        self.jointToolsMainLayout.addRow("", self.jointCreateChainLayout)
    # Connections
        self.jointHierarchyButton.clicked.connect(lambda: self.selectJointHierarchy())
        self.jointAtCVsButton.clicked.connect(lambda: self.jointsAtCVs())
        self.jointAtObjectsButton.clicked.connect(lambda: self.jointsAtObjects())
        self.jointCreateChainButton.clicked.connect(lambda: self.createJointChain())
        self.jointAxisSelector.currentIndexChanged.connect(lambda: self.setJointAxis())
        self.jointNumberInput.textEdited.connect(lambda: self.setJointNumber())
        self.jointSpacingInput.textEdited.connect(lambda: self.setJointSpacing())
        self.jointOrientationSelector.currentIndexChanged.connect(lambda: self.setJointOrientation())
        self.jointSecondarySelector.currentIndexChanged.connect(lambda : self.setJointSecondary())
        self.jointResetButton.clicked.connect(lambda: self.resetJointTools())

    # Constraint Tools GUI
    def constraintToolsCreateGUI(self):
    # Widgets
        self.createParentConstraintCheckbox = QtWidgets.QCheckBox("Parent")
        self.createParentConstraintCheckbox.setChecked(True)
        self.createPointConstraintCheckbox = QtWidgets.QCheckBox("Point")
        self.createOrientConstraintCheckbox = QtWidgets.QCheckBox("Orient")
        self.createScaleConstraintCheckbox = QtWidgets.QCheckBox("Scale")

        self.constraintOffsetCheckbox = QtWidgets.QCheckBox("Maintain Offset")
        self.constraintOffsetCheckbox.setChecked(True)
        self.constraintAllowMultipleCheckbox = QtWidgets.QCheckBox("Allow Multiple")
        self.constraintAllowMultipleCheckbox.setStatusTip("Allows object to be constrained to multiple objects")
        self.constraintAllowMultipleCheckbox.setWhatsThis("Unless checked, this prevents objects from having multiple, same type constraints applied.")
        self.createConstraintsButton = QtWidgets.QPushButton("Create Constraints")

        self.bakeConstraintsStartLabel = QtWidgets.QLabel("Bake Start Time")
        self.bakeConstraintsStartInput = QtWidgets.QLineEdit()
        self.bakeConstraintsStartInput.setText("1.0")
        floatValidator = QtGui.QDoubleValidator()
        floatValidator.setDecimals(1)
        self.bakeConstraintsStartInput.setValidator(floatValidator)
        self.bakeConstraintsGetAnimStartButton = QtWidgets.QPushButton("Get Animation Start")
        self.bakeConstraintsGetPlaybackStartButton = QtWidgets.QPushButton("Get Playback Start")

        self.bakeConstraintsEndLabel = QtWidgets.QLabel("Bake End Time")
        self.bakeConstraintsEndInput = QtWidgets.QLineEdit()
        self.bakeConstraintsEndInput.setText("200.0")
        self.bakeConstraintsEndInput.setValidator(floatValidator)
        self.bakeConstraintsGetAnimEndButton = QtWidgets.QPushButton("Get Animation End")
        self.bakeConstraintsGetPlaybackEndButton = QtWidgets.QPushButton("Get Playback End")

        self.bakeConstraintsButton = QtWidgets.QPushButton("Bake Constraints to Anim")
        self.bakeConstraintsButton.setStatusTip("Replaces constraints with animation")
        self.bakeConstraintsButton.setWhatsThis("Motion derived from constraints on all selected objects will be converted to keyframes from Bake Start Time to Bake End Time and constraints deleted.")
        self.bakeLocatorsButton = QtWidgets.QPushButton("Bake Locators For AE")
        self.bakeLocatorsButton.setStatusTip("Bake locators for use in After Effects")
        self.bakeLocatorsButton.setWhatsThis(
            f"Creates constraints between first selected object and subsequently selected locators. \n"
            f"Bakes animation derived from constraints from Start Bake Time to End Bake Time into keyframes and deletes constraints. \n"
            f"Only translation information is baked for After Effects. Rotation is not needed, and any translation derived from the parent object's scale is accounted for."
        )

        self.findParentButton = QtWidgets.QPushButton("Find Constraint Parent(s)")
        self.findParentButton.setStatusTip("Finds the constraint parent(s)")
        self.findParentButton.setWhatsThis("Finds what object(s) the current selection is constrained to and populates a list for optional selection.")
        self.constraintParentsInput = QtWidgets.QLineEdit()
        self.constraintParentsInput.setText("Constraint Parent Objects")
        self.selectConstraintParentsButton = QtWidgets.QPushButton("Select Constraint Parents")

        self.findChildrenButton = QtWidgets.QPushButton("Find Constraint Children")
        self.findChildrenButton.setStatusTip("Finds objects currently constrained to selection")
        self.findChildrenButton.setWhatsThis("Finds any object constrained to current selection and populates a list for optional selection.")
        self.constraintChildrenInput = QtWidgets.QLineEdit()
        self.constraintChildrenInput.setText("Constrained Children Objects")
        self.selectConstraintChildrenButton = QtWidgets.QPushButton("Select Constraint Children")
    # Layouts
        self.createConstraintsLayout = QtWidgets.QHBoxLayout()
        self.createConstraintsLayout.addWidget(self.createParentConstraintCheckbox)
        self.createConstraintsLayout.addWidget(self.createPointConstraintCheckbox)
        self.createConstraintsLayout.addWidget(self.createOrientConstraintCheckbox)
        self.createConstraintsLayout.addWidget(self.createScaleConstraintCheckbox)
        
        self.constraintOptionsLayout = QtWidgets.QHBoxLayout()
        self.constraintOptionsLayout.addWidget(self.constraintOffsetCheckbox)
        self.constraintOptionsLayout.addWidget(self.constraintAllowMultipleCheckbox)
        
        self.constraintExecuteLayout = QtWidgets.QHBoxLayout()
        self.constraintExecuteLayout.addWidget(self.createConstraintsButton)

        self.bakeConstraintsLayout = QtWidgets.QGridLayout()
        self.bakeConstraintsLayout.addWidget(self.bakeConstraintsStartLabel, 0,0)
        self.bakeConstraintsLayout.addWidget(self.bakeConstraintsStartInput, 0,1)
        self.bakeConstraintsLayout.addWidget(self.bakeConstraintsGetAnimStartButton, 0,2)
        self.bakeConstraintsLayout.addWidget(self.bakeConstraintsGetPlaybackStartButton, 0,3)

        self.bakeConstraintsLayout.addWidget(self.bakeConstraintsEndLabel, 1,0)
        self.bakeConstraintsLayout.addWidget(self.bakeConstraintsEndInput, 1,1)
        self.bakeConstraintsLayout.addWidget(self.bakeConstraintsGetAnimEndButton, 1,2)
        self.bakeConstraintsLayout.addWidget(self.bakeConstraintsGetPlaybackEndButton, 1,3)

        self.bakeConstraintsLayout.addWidget(self.bakeConstraintsButton, 2,0)
        self.bakeConstraintsLayout.addWidget(self.bakeLocatorsButton, 2,1)
        self.bakeConstraintsLayout.addWidget(self.findParentButton, 3,0)
        self.bakeConstraintsLayout.addWidget(self.constraintParentsInput, 3,1)
        self.bakeConstraintsLayout.addWidget(self.selectConstraintParentsButton, 3,2)

        self.bakeConstraintsLayout.addWidget(self.findChildrenButton, 4,0)
        self.bakeConstraintsLayout.addWidget(self.constraintChildrenInput, 4,1)
        self.bakeConstraintsLayout.addWidget(self.selectConstraintChildrenButton, 4,2)

        self.constraintToolsMainLayout = QtWidgets.QFormLayout(self.constraintToolsTab)
        self.constraintToolsMainLayout.addRow("", self.createConstraintsLayout)
        self.constraintToolsMainLayout.addRow("", self.constraintOptionsLayout)
        self.constraintToolsMainLayout.addRow("", self.constraintExecuteLayout)
        self.constraintToolsMainLayout.addRow("", self.bakeConstraintsLayout)
    # Connections
        self.createParentConstraintCheckbox.stateChanged.connect(lambda: self.setTransformConstraintType("parent"))
        self.createPointConstraintCheckbox.stateChanged.connect(lambda: self.setTransformConstraintType("point"))
        self.createOrientConstraintCheckbox.stateChanged.connect(lambda: self.setTransformConstraintType("orient"))
        self.createScaleConstraintCheckbox.stateChanged.connect(lambda: self.setScaleConstraint())
        self.constraintOffsetCheckbox.stateChanged.connect(lambda: self.setMaintainOffset())
        self.constraintAllowMultipleCheckbox.stateChanged.connect(lambda: self.setAllowMultipleConstraints())
        self.createConstraintsButton.clicked.connect(lambda: self.createMultipleConstraints())
        self.bakeConstraintsGetAnimStartButton.clicked.connect(lambda: self.getAnimationStart())
        self.bakeConstraintsGetPlaybackStartButton.clicked.connect(lambda: self.getPlaybackStart())
        self.bakeConstraintsGetAnimEndButton.clicked.connect(lambda: self.getAnimationEnd())
        self.bakeConstraintsGetPlaybackEndButton.clicked.connect(lambda: self.getPlaybackEnd())
        self.bakeConstraintsButton.clicked.connect(lambda: self.convertConstraintsToAnim())
        self.bakeLocatorsButton.clicked.connect(lambda: self.bakeLocatorsForAE())
        self.findParentButton.clicked.connect(lambda: self.findConstraintParent())
        self.selectConstraintParentsButton.clicked.connect(lambda: self.selectConstraintParents())
        self.findChildrenButton.clicked.connect(lambda: self.findConstraintChildren())
        self.selectConstraintChildrenButton.clicked.connect(lambda: self.selectConstraintChildren())

    # Scene Info GUI
    def sceneInfoCreateGUI(self):
    # Widgets
        self.sceneApplicationLabel = QtWidgets.QLabel("Application :")
        self.sceneApplicationFeedback = QtWidgets.QLabel("")

        self.sceneVersionLabel = QtWidgets.QLabel("Version :")
        self.sceneVersionFeedback = QtWidgets.QLabel("")

        self.sceneProductLabel = QtWidgets.QLabel("Product :")
        self.sceneProductFeedback = QtWidgets.QLabel("")

        self.sceneOSVersionLabel = QtWidgets.QLabel("OS Version :")
        self.sceneOSVersionFeedback = QtWidgets.QLabel("")
        
        self.sceneCutLabel = QtWidgets.QLabel("Cut :")
        self.sceneCutFeedback = QtWidgets.QLabel("")

        self.sceneInfoButton = QtWidgets.QPushButton("Scene Info")
    # Layouts
        self.sceneFeedbackLayout = QtWidgets.QGridLayout()
        self.sceneFeedbackLayout.addWidget(self.sceneApplicationLabel, 0, 0)
        self.sceneFeedbackLayout.addWidget(self.sceneApplicationFeedback, 0, 1)
        self.sceneFeedbackLayout.addWidget(self.sceneVersionLabel,1,0)
        self.sceneFeedbackLayout.addWidget(self.sceneVersionFeedback,1,1)
        self.sceneFeedbackLayout.addWidget(self.sceneProductLabel,2,0)
        self.sceneFeedbackLayout.addWidget(self.sceneProductFeedback,2,1)
        self.sceneFeedbackLayout.addWidget(self.sceneOSVersionLabel,3,0)
        self.sceneFeedbackLayout.addWidget(self.sceneOSVersionFeedback,3,1)
        self.sceneFeedbackLayout.addWidget(self.sceneCutLabel,4,0)
        self.sceneFeedbackLayout.addWidget(self.sceneCutFeedback,4,1)

        self.sceneFeedbackButtonLayout = QtWidgets.QHBoxLayout()
        self.sceneFeedbackButtonLayout.addWidget(self.sceneInfoButton)

        self.sceneInfoMainLayout = QtWidgets.QFormLayout(self.sceneInfoTab)
        self.sceneInfoMainLayout.addRow("", self.sceneFeedbackLayout)
        self.sceneInfoMainLayout.addRow("", self.sceneFeedbackButtonLayout)
    # Connections
        self.sceneInfoButton.clicked.connect(lambda:self.getSceneInfo())

    # UI Tools Methods______________________
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
    
# Creation Tools methods________________________
    # Ensures vertices are selected for further tools usage
    def selectVertices(self):
        self.vertexArray = cmds.filterExpand(selectionMask=31) or []

    def createLocatorsAtVerts(self):
        self.selectVertices()

        if not self.vertexArray:
            openErrorWindow("Select at least one vertex to place locator.")
            raise ValueError("Select at least one vertex to place locator.")
        self.checkGroups("locator")
        
        positions = [cmds.pointPosition(vert) for vert in self.vertexArray]
        # Create locators at each selected vertex position 
        for pos in positions:
            currentLocator = cmds.spaceLocator()[0]
            cmds.move(pos[0], pos[1], pos[2], currentLocator)
            cmds.xform(currentLocator, pivots=(pos[0], pos[1], pos[2]), worldSpace=True)
            cmds.parent(currentLocator, self.groupType)

        cmds.select(clear=True)
    
    def locatorAtCenterVerts(self):
        self.selectVertices()
        if len(self.vertexArray) < 2:
            openErrorWindow(f"A minimum of 2 vertices is required. Found {len(self.vertexArray)}")
            raise ValueError(f"Minimum of 2 vertices required, found {len(self.vertexArray)}")
        
        self.checkGroups("locator")
        
        tempCluster, tempHandle = cmds.cluster(self.vertexArray)
        centeredLoc = cmds.spaceLocator()
        tempConstraint = cmds.pointConstraint(tempHandle, centeredLoc, maintainOffset = False)
        cmds.delete(tempConstraint,tempCluster)
        self.vertexArray = []

        cmds.parent(centeredLoc, self.groupType)

    def setUseCustomColor(self):
        self.useCustomColorChoice = self.useCustomColorCheckBox.isChecked()
        return self.useCustomColorChoice
    
    # Updates UI color and sets result as color choice when creating or editing curves
    def setColorSlider(self):
        self.customColorSliderIndex = self.customColorSlider.value()
        indexDictionary = {
            0:"background-Color: rgb(130,130,130);",#mid gray
            1:"background-Color: rgb(0,0,0);",#black
            2:"background-Color: rgb(64,64,64);",#gray
            3:"background-Color: rgb(153,153,153);",#light gray
            4:"background-Color: rgb(155,0,40);",#dark red
            5:"background-Color: rgb(0,4,96);",#dark blue
            6:"background-Color: rgb(0,0,255);",#blue
            7:"background-Color: rgb(0,70,25);",#dark green
            8:"background-Color: rgb(38,0,67);",#dark purple
            9:"background-Color: rgb(200,0,200);",#magenta
            10:"background-Color: rgb(138,72,51);",#light brown
            11:"background-Color: rgb(63,35,31);",#dark brown
            12:"background-Color: rgb(153,38,0);",#red orange
            13:"background-Color: rgb(255,0,0);",#red
            14:"background-Color: rgb(0,255,0);",#green
            15:"background-Color: rgb(0,65,153);",#light blue
            16:"background-Color: rgb(255,255,255);",#white
            17:"background-Color: rgb(255,255,0);",#yellow
            18:"background-Color: rgb(100,220,255);",#light blue
            19:"background-Color: rgb(67,255,163);",#light pastel green
            20:"background-Color: rgb(255,176,176);",#pink
            21:"background-Color: rgb(228,172,121);",#orange
            22:"background-Color: rgb(255,255,99);",#green yellow
            23:"background-Color: rgb(0,153,84);",#dark pastel green
            24:"background-Color: rgb(161,106,48);",#orange brown
            25:"background-Color: rgb(158,161,48);",#yellow green
            26:"background-Color: rgb(104,161,48);",#green yellow
            27:"background-Color: rgb(48,161,93);",#mid pastel green
            28:"background-Color: rgb(48,161,161);",#blue green
            29:"background-Color: rgb(48,103,161);",#blue gray
            30:"background-Color: rgb(111,48,161);",#indigo
            31:"background-Color: rgb(161,48,106);",#pink purple
        }
        self.customColorDialog.setStyleSheet(indexDictionary[self.customColorSliderIndex])
        return self.customColorSliderIndex

    # Changes color of selected nurbs curve
    def setCustomControlColor(self):
        currentSelection = cmds.ls(selection = True)
        if not currentSelection:
            openErrorWindow("Select a NURBS Curve to change its color.")
            raise ValueError("Select a NURBS Curve to change its color.")
        for sel in currentSelection:
            shape = cmds.listRelatives(sel, shapes = True)
            if shape:
                # set color choice to UI's current color selection
                self.customColorChoice = self.setColorSlider()
                for s in shape:
                    type = cmds.objectType(s)
                    if type != "nurbsCurve":
                        openErrorWindow(f"{sel} is not a nurbs curve")
                        raise ValueError(f"{sel} is not a nurbs curve")
                    else:
                        
                        cmds.setAttr((f"{s}.overrideEnabled"),True)
                        cmds.setAttr((f"{s}.overrideColor"), self.customColorChoice)
            else:
                openErrorWindow(f"{sel} has no shape node. Select at least 1 Nurbs Curve")
                raise ValueError(f"{sel} has no shape node")
        
        cmds.select(clear=True)

    # Create Global control
    def createGlobalControl(self):
        positions = [
            (-1, 0, -1),
            (-1, 0, -3),
            (-2, 0, -3),
            (0, 0, -5),
            (2, 0, -3),
            (1, 0, -3),
            (1, 0, -1),
            (3, 0, -1),
            (3, 0, -2),
            (5, 0, 0),
            (3, 0, 2),
            (3, 0, 1), 
            (1, 0, 1), 
            (1, 0, 3), 
            (2, 0, 3), 
            (0, 0, 5), 
            (-2, 0, 3), 
            (-1, 0, 3), 
            (-1, 0, 1), 
            (-3, 0, 1), 
            (-3, 0, 2), 
            (-5, 0, 0), 
            (-3, 0, -2), 
            (-3, 0, -1), 
            (-1, 0, -1)
        ]
        
        self.checkGroups("control")

        groupNumber = 0

        while True:
            groupName = f"GlobalConrol_{groupNumber}_Ctrl_Grp"
            nullGroupName = f"GlobalControl_{groupNumber}_Ctrl_Null_Grp"
            controlName = f"GlobalControl_{groupNumber}_Ctrl"
            if not cmds.objExists(groupName):
                globalControlGroup = cmds.group(empty=True, name=groupName)
                globalControlNullGroup = cmds.group(empty=True, name=nullGroupName)
                globalControlCurve = cmds.curve(degree = 1, p=positions, name=controlName)
                cmds.parent(globalControlNullGroup, globalControlGroup)
                cmds.parent(globalControlCurve, globalControlNullGroup)
                break
            else:
                groupNumber += 1

        cmds.parent(globalControlGroup, self.groupType)

        if self.useCustomColorChoice:
            self.customColorChoice = self.setColorSlider()
            controlShape = cmds.listRelatives(globalControlCurve, shapes=True)[0]
            cmds.setAttr((f"{controlShape}.overrideEnabled"),True)
            cmds.setAttr((f"{controlShape}.overrideColor"), self.customColorChoice)

        cmds.select(clear=True)
    
    # Combines selected curves under a single transform to create custom animation controls
    def createCustomControl(self):
        selectedTransforms = cmds.ls(selection=True, type="transform")

        selectedCurves = [
            transform for transform in selectedTransforms
            if cmds.listRelatives(transform, type="nurbsCurve", children=True)
        ]
        
        if len(selectedCurves) < 2:
            openErrorWindow("Select a minimum of 2 NURBS curves")
            raise ValueError("Select a minimum of 2 NURBS curves.")
        
        #freeze transforms
        cmds.makeIdentity(selectedCurves, apply = True)
        cmds.DeleteHistory(selectedCurves)

        tempShapes = cmds.listRelatives(selectedCurves, shapes = True)
        
        customControlGroupName = f"{selectedTransforms[0]}_Ctrl"
        customControl = cmds.group(empty = True, name=customControlGroupName)

        cmds.parent(tempShapes, customControl, relative=True, shape=True)
        cmds.delete(selectedCurves)
        cmds.xform(customControl, centerPivots=True)
        cmds.move(0,0,0, customControl, rotatePivotRelative=True)
        
        customControlNullName = f"{customControl}_Null_Grp"
        customControlNull = cmds.group(empty=True, name=customControlNullName)
        
        tempConstraint = cmds.parentConstraint(customControlNull, customControl, maintainOffset = True)
        cmds.delete(tempConstraint)
        cmds.makeIdentity(customControl, apply=True)
        
        # Update viewport, otherwise while curve has been created correctly, it doesn't look that way.
        cmds.ogs(reset=True)

        self.checkGroups("control")

        cmds.parent(customControlNull, self.groupType)
            
        cmds.parent(customControl, customControlNull)

        if self.useCustomColorChoice:
            self.customColorChoice = self.setColorSlider()
            controlShapes = cmds.listRelatives(customControl, shapes=True)
            for s in controlShapes:
                cmds.setAttr((f"{s}.overrideEnabled"),True)
                cmds.setAttr((f"{s}.overrideColor"), self.customColorChoice)

        cmds.select(clear=True)
    
    # Selection Tools Methods___________________________
    def getSearchCurrent(self):
        self.selectSearchCurrentChoice = self.selectSearchCurrentCheckbox.isChecked()
        return self.selectSearchCurrentChoice
    
    def getAddToSelection(self):
        self.addToSelectionChoice = self.selectAddToCheckbox.isChecked()
        return self.addToSelectionChoice
    
    def selectHierarchy(self):
        currentSelection = cmds.ls(selection=True)
        if not currentSelection:
            openErrorWindow("Select an object.")
            raise ValueError("Select an object.")
        if not self.addToSelectionChoice:
            cmds.select(hierarchy=True)
        else:
            cmds.select(hierarchy=True, add=True)

    def findRoot(self):
        currentSelection = cmds.ls(selection=True)
        rootNode = None
        if not currentSelection:
            openErrorWindow("Select an object to find its root node.")
            raise ValueError("Select an object to find its root node.")
        else:
            rootNode = currentSelection[0]

        while True:
            parentNode = cmds.listRelatives(rootNode, parent=True)
            if parentNode and rootNode:
                rootNode = parentNode[0]
            else:
                break
        
        if not self.addToSelectionChoice:
            cmds.select(rootNode)
        else:
            cmds.select(rootNode, add=True)

    def selectAllMeshes(self):
        # Helper function to select parents of meshes
        def getMeshParents(meshes):
            parents = []
            for mesh in meshes:
                parent = cmds.listRelatives(mesh, parent=True)
                if parent:
                    parents.append(parent[0])
            return parents

        # If 'selectSearchCurrentChoice' is False, select all meshes in the scene
        if not self.selectSearchCurrentChoice:
            if not self.addToSelectionChoice:
                cmds.select(clear=True)

            allMeshes = cmds.ls(type="mesh")
            if not allMeshes:
                self.selectFeedbackOutput.setText("0 Polygon Meshes found.")
                return  # Early exit since there are no meshes

            # Select all mesh parents in one go
            parents = getMeshParents(allMeshes)
            cmds.select(parents, add=True)
            
            number = len(parents)
            self.selectFeedbackOutput.setText(f"{number} Polygon Meshes in scene.")
        
        # If 'selectSearchCurrentChoice' is True, search descendants of selected objects
        else:
            selection = cmds.ls(selection=True)
            if not selection:
                openErrorWindow("Select an object to search its descendants for Polygon Meshes")
                return  # Early exit if nothing is selected

            polySet = set()
            for obj in selection:
                descendants = cmds.listRelatives(obj, allDescendents=True, type="mesh")
                if descendants:
                    polySet.update(descendants)
            
            if not polySet:
                self.selectFeedbackOutput.setText("No descendant Polygon Meshes found.")
                return  # Early exit if no descendant meshes found

            # Select all mesh parents in one go
            parents = getMeshParents(polySet)
            cmds.select(parents, replace=True)

            if self.addToSelectionChoice:
                cmds.select(selection, add=True)

            number = len(parents)
            self.selectFeedbackOutput.setText(f"{number} Meshes under selection.")

    def selectAllCurves(self):
        def getCurveParents(curves):
            parents = []
            for curve in curves:
                parent = cmds.listRelatives(curve, parent=True)
                if parent:
                    parents.append(parent[0])
            return parents
        # If 'selectSearchCurrentChoice' is False, select all meshes in the scene
        if not self.selectSearchCurrentChoice:
            if not self.addToSelectionChoice:
                cmds.select(clear=True)
            
            allCurves = cmds.ls(type = "nurbsCurve")
            if not allCurves:
                self.selectFeedbackOutput.setText("0 Curves found.")
                return

            parents = getCurveParents(allCurves)
            cmds.select(parents, add=True)

            number = len(parents)
            self.selectFeedbackOutput.setText(f"{number} Curves in scene.")

        # If 'selectSearchCurrentChoice' is True, search descendants of selected objects
        else:
            selection = cmds.ls(selection=True)
            if not selection:
                openErrorWindow("Select an object to search its descendants for Curves.")
                return
            curveSet = set()
            for obj in selection:
                descendants = cmds.listRelatives(obj, allDescendents = True, type="nurbsCurve")
                if descendants:
                    curveSet.update(descendants)
            
            if not curveSet:
                self.selectFeedbackOutput.setText("No descendant Curves found.")
                return
            
            parents = getCurveParents(curveSet)
            cmds.select(parents, replace=True)

            if self.addToSelectionChoice:
                cmds.select(selection, add=True)

            number = len(parents)
            self.selectFeedbackOutput.setText(f"{number} Curves under selection.")

    def selectAllNurbsSurfaces(self):
        def getCurveParents(curves):
            parents = []
            for curve in curves:
                parent = cmds.listRelatives(curve, parent=True)
                if parent:
                    parents.append(parent[0])
            return parents
        # If 'selectSearchCurrentChoice' is False, select all meshes in the scene
        if not self.selectSearchCurrentChoice:
            if not self.addToSelectionChoice:
                cmds.select(clear=True)
            
            allSurfaces = cmds.ls(type = "nurbsSurface")
            if not allSurfaces:
                self.selectFeedbackOutput.setText("0 NURBS found.")
                return

            parents = getCurveParents(allSurfaces)
            cmds.select(parents, add=True)

            number = len(parents)
            self.selectFeedbackOutput.setText(f"{number} NURBS in scene.")

        # If 'selectSearchCurrentChoice' is True, search descendants of selected objects
        else:
            selection = cmds.ls(selection=True)
            if not selection:
                openErrorWindow("Select an object to search its descendants for NURBS.")
                return
            nurbsSet = set()
            for obj in selection:
                descendants = cmds.listRelatives(obj, allDescendents = True, type="nurbsSurface")
                if descendants:
                    nurbsSet.update(descendants)
            
            if not nurbsSet:
                self.selectFeedbackOutput.setText("No descendant NURBS found.")
                return
            
            parents = getCurveParents(nurbsSet)
            cmds.select(parents, replace=True)

            if self.addToSelectionChoice:
                cmds.select(selection, add=True)

            number = len(parents)
            self.selectFeedbackOutput.setText(f"{number} NURBS under selection.")
        
    def selectLights(self, lightTypes):
        selectedLights = set()
        
        for lightType in lightTypes:
            lights = cmds.ls(type=lightType)
            if lights:
                selectedLights.update(lights)
        
        if not selectedLights:
            if any(light.startswith("light") for light in lightTypes):
                self.selectFeedbackOutput.setText("No Maya Lights found")

            if any(light.startswith("Redshift") for light in lightTypes):
                self.selectFeedbackOutput.setText("No Redshift Lights found")

            if any(light.startswith("VRay") for light in lightTypes):
                self.selectFeedbackOutput.setText("No VRay Lights found")

            if any(light.startswith("light") for light in lightTypes) and any(light.startswith("Redshift") for light in lightTypes) and any(light.startswith("VRay") for light in lightTypes):
                self.selectFeedbackOutput.setText("No Lights found")
            return set()

        if not self.addToSelectionChoice:
            cmds.select(clear=True)
        
        for light in selectedLights:
            currentRelative = cmds.listRelatives(light, parent=True)
            if currentRelative:
                cmds.select(currentRelative, add=True)
        
        return selectedLights

    def selectAllMayaLights(self):
        self.allMayaLights = self.selectLights(["light"])
        number = str(len(self.allMayaLights))
        self.selectFeedbackOutput.setText(f"{number} Maya Lights in scene.")

    def selectAllRedshiftLights(self):
        lightTypes = ["RedshiftPhysicalLight", "RedshiftDomeLight", "RedshiftIESLight", "RedshiftPortalLight" ]
        self.redshiftLightsSet = self.selectLights(lightTypes)
        number = str(len(self.redshiftLightsSet))
        self.selectFeedbackOutput.setText(f"{number} Redshift Lights in scene.")

    def selectAllVRayLights(self):
        lightTypes = ["VRayLightRectShape", "VRayLightDomeShape", "VRayLightIESShape", "VRayLightSphereShape"]
        self.vRayLightsSet = self.selectLights(lightTypes)
        number = str(len(self.vRayLightsSet))
        self.selectFeedbackOutput.setText(f"{number} VRay Lights in scene.")

    def selectAllLights(self):

        allLightTypes = [
            "light",                    # Maya lights
            "RedshiftPhysicalLight",    #Redshift lights
            "RedshiftDomeLight", 
            "RedshiftIESLight", 
            "RedshiftPortalLight",          
            "VRayLightRectShape",       #VRay lights
            "VRayLightDomeShape", 
            "VRayLightIESShape", 
            "VRayLightSphereShape"          
        ]

        if not self.addToSelectionChoice:
            cmds.select(clear=True)

        everyLight = self.selectLights(allLightTypes)

        totalLights = str(len(everyLight))
        self.selectFeedbackOutput.setText(f"{totalLights} Lights in scene.")

    def selectAnimationCurves(self):
        if not self.selectSearchCurrentChoice: # Search entire scene
            allAnimCurves = cmds.ls(type="animCurve")
            if not allAnimCurves:
                self.selectFeedbackOutput.setText("No Animation found.")
            if not self.addToSelectionChoice:
                cmds.select(allAnimCurves)
            else:
                cmds.select(allAnimCurves, add=True)
        else:
            selection = cmds.ls(selection=True)
            # Initialize a set to hold the selection's  and descendents' anim curves
            if not selection:
                openErrorWindow("Select an object to search its descendents for animation")
                return
            
            animCurvesSet = set()
            
            for obj in selection:
                # make sure selected object is included
                objAnim = cmds.listConnections(obj, type="animCurve")
                if objAnim:
                    animCurvesSet.update(objAnim)
                
                children = cmds.listRelatives(obj, allDescendents = True)
                if children:
                    for c in children:
                        animCurve = cmds.listConnections(c, type="animCurve")
                        if animCurve:
                            animCurvesSet.update(animCurve)
            cmds.select(animCurvesSet)

    def selectAllJointRoots(self):
        # If 'selectSearchCurrentChoice' is False, select all joint roots in the scene
        if not self.selectSearchCurrentChoice:
            if not self.addToSelectionChoice:
                cmds.select(clear=True)
            allJoints = cmds.ls(type="joint")
            if not allJoints:
                self.selectFeedbackOutput.setText("0 Joints found in scene.")
            visitedJoints = set()
            
            for j in allJoints:
                rootJoint = j
                
                while True:
                    parentJoint = cmds.listRelatives(rootJoint, parent=True, type="joint")
                    if parentJoint:
                        rootJoint = parentJoint[0]
                    else:
                        break
                
                if rootJoint not in visitedJoints:
                    cmds.select(rootJoint, add=True)
                    visitedJoints.add(rootJoint)

            number = str(len(visitedJoints))
            self.selectFeedbackOutput.setText(f"{number} Joint Chains in scene.")
        # If 'selectSearchCurrentChoice' is True, search descendants of selected objects
        else:
            selection = cmds.ls(selection=True)
            if not selection:
                openErrorWindow("Select an object to search its descendants for Joints")
                return
            
            jointSet = set()
            for obj in selection:
                descendants = cmds.listRelatives(obj, allDescendents=True, type="joint")
                if descendants:
                    jointSet.update(descendants)
            if not jointSet:
                self.selectFeedbackOutput.setText("No descendant Joints found.")
                return
            visitedJoints = set()
            
            for j in jointSet:
                rootJoint = j
                while True:
                    parentJoint = cmds.listRelatives(rootJoint, parent=True, type="joint")
                    if parentJoint:
                        rootJoint = parentJoint[0]
                    else:
                        break
                if rootJoint not in visitedJoints:
                    cmds.select(rootJoint, add=True)
                    visitedJoints.add(rootJoint)
            number = str(len(visitedJoints))
            self.selectFeedbackOutput.setText(f"{number} Joint Chains under selection.")

    def selectBlendshapeMeshes(self):
        currentSelection = cmds.ls(selection=True)
        
        targetMeshes = []
        if currentSelection:

            for obj in currentSelection:
                historyNodes = cmds.listHistory(obj)

                blendshapeNodes = cmds.ls(historyNodes, type="blendShape")
                
                for bsn in blendshapeNodes:

                    targetNames = cmds.blendShape(bsn, query=True, target=True)

                    if targetNames:
                        targetMeshes.extend(targetNames)
                    else:
                        # Let user know which object in the selection has missing target meshes.
                        openErrorWindow(f"{obj} has a blendShape node, but targets may have been deleted.\nAll other blendShape targets selected.")
                        print(f"{obj} has a blendShape node, but targets may have been deleted.\nAll other blendShape targers selected.")
            
            # If we found any target meshes, select them accounting for if "Add To Selection" is checked
            if targetMeshes:
                if not self.addToSelectionChoice:
                    cmds.select(targetMeshes)
                else:
                    cmds.select(targetMeshes, add=True)
            else:
                # If the selection has a blendshape node, but no targets, let the user know which object's target meshes are missing
                if blendshapeNodes:
                    for bsn in blendshapeNodes:
                        if not targetNames:
                            openErrorWindow(f"{currentSelection[0]} has a blendShape node, but targets may have been deleted")
                            print(f"{currentSelection[0]} has a blendShape node, but targets may have been deleted.")
                else:
                    openErrorWindow("No blendShape target meshes found on current seleciton.")
                    print("No blendShape not found on current selection.")
        
            number = str(len(targetMeshes))
            self.selectFeedbackOutput.setText(f"{number} BlendShape Objects in scene.")
        else:
            openErrorWindow("Select an object to begin search.")
            allMeshes = cmds.ls(type="mesh")
            if allMeshes:
                allMeshesHistoryNodes = cmds.listHistory(allMeshes)
                allMeshesBlendshapeNodes = cmds.ls(allMeshesHistoryNodes, type="blendShape")
                number = str(len(allMeshesBlendshapeNodes))
            else:
                number = 0
            self.selectFeedbackOutput.setText(f"{number} BlendShape Nodes in scene.")
            print("Select an object to begin search.")

    def selectAllLocators(self):
        # Helper function to select parents of meshes
        def getLocatorParents(locators):
            parents = []
            for loc in locators:
                parent = cmds.listRelatives(loc, parent=True)
                if parent:
                    parents.append(parent[0])
            return parents

        # If 'selectSearchCurrentChoice' is False, select all meshes in the scene
        if not self.selectSearchCurrentChoice:
            if not self.addToSelectionChoice:
                cmds.select(clear=True)

            allLocators = cmds.ls(type="locator")
            if not allLocators:
                self.selectFeedbackOutput.setText("0 Locators found.")

            # Select all mesh parents in one go
            parents = getLocatorParents(allLocators)
            cmds.select(parents, add=True)
            
            number = len(parents)
            self.selectFeedbackOutput.setText(f"{number} Locators in scene.")
        
        # If 'selectSearchCurrentChoice' is True, search descendants of selected objects
        else:
            selection = cmds.ls(selection=True)
            if not selection:
                openErrorWindow("Select an object to search its descendants for Locators")
                return  # Early exit if nothing is selected

            locatorSet = set()
            for obj in selection:
                descendants = cmds.listRelatives(obj, allDescendents=True, type="locator")
                if descendants:
                    locatorSet.update(descendants)
            
            if not locatorSet:
                self.selectFeedbackOutput.setText("No descendant Locators found.")

            # Select all mesh parents in one go
            parents = getLocatorParents(locatorSet)
            cmds.select(parents, replace=True)

            if self.addToSelectionChoice:
                cmds.select(selection, add=True)

            number = len(parents)
            self.selectFeedbackOutput.setText(f"{number} Locators under selection.")

    def selectAllConstraints(self):
        # If 'selectSearchCurrentChoice' is False, select all constraints in the scene
        if not self.selectSearchCurrentChoice:
            if not self.addToSelectionChoice:
                cmds.select(clear=True)
            allConstraints = cmds.ls(type="constraint")
            if not allConstraints:
                self.selectFeedbackOutput.setText("0 Constraints found")
                return
            if not self.addToSelectionChoice:
                cmds.select(allConstraints)
            else:
                cmds.select(allConstraints, add=True)
            number = str(len(allConstraints))
            self.selectFeedbackOutput.setText(f"{number} Constraints in scene.")
        else:
            selection = cmds.ls(selection=True)
            if not selection:
                openErrorWindow("Select an object to search its descendants for Constraints")
                return
            
            constraintSet = set()
            for obj in selection:
                descendants = cmds.listRelatives(obj, allDescendents=True, type="constraint")
                if descendants:
                    constraintSet.update(descendants)

            if not constraintSet:
                self.selectFeedbackOutput.setText("No descendant Constraints found.")
                return

            cmds.select(constraintSet, replace=True)
            if self.addToSelectionChoice:
                cmds.select(selection, add=True)
            
            number = len(constraintSet)
            self.selectFeedbackOutput.setText(f"{number} Constraints under selection.")
    
    def selectAllIKHandles(self):
        # If 'selectSearchCurrentChoice' is False, select all IK Handles in the scene
        if not self.selectSearchCurrentChoice:
            if not self.addToSelectionChoice:
                cmds.select(clear=True)
            allIKHandles = cmds.ls(type="ikHandle")
            if not allIKHandles:
                self.selectFeedbackOutput.setText("0 IK Handles found")
                return
            if not self.addToSelectionChoice:
                cmds.select(allIKHandles)
            else:
                cmds.select(allIKHandles, add=True)
            number = str(len(allIKHandles))
            self.selectFeedbackOutput.setText(f"{number} IK Handles in scene.")
        else:
            selection = cmds.ls(selection=True)
            if not selection:
                openErrorWindow("Select an object to search its descendants for IK Handles")
                return
            
            ikHandleSet = set()
            for obj in selection:
                descendants = cmds.listRelatives(obj, allDescendents=True, type="ikHandle")
                if descendants:
                    ikHandleSet.update(descendants)

            if not ikHandleSet:
                self.selectFeedbackOutput.setText("No descendant IK Handles found.")
                return

            cmds.select(ikHandleSet, replace=True)
            if self.addToSelectionChoice:
                cmds.select(selection, add=True)
            
            number = len(ikHandleSet)
            self.selectFeedbackOutput.setText(f"{number} IK Handles under selection.")

    # Curve Tools Methods______________
    def setCurveObjectCleanup(self):
        self.objectCleanup = self.cleanupObjectsCheckbox.isChecked()
        return self.objectCleanup
    
    def createCurveAtObjects(self, cleanup = False):
        objectPositions = []
        cleanup = self.objectCleanup
        currentSelection = cmds.ls(selection=True, type="transform")
        
        if len(currentSelection) < 4:
            openErrorWindow(f"A minimum of 4 objects is required. Found {len(currentSelection)}.")
            raise ValueError(f"Minimum of 4 objects required, found {len(currentSelection)}")
        
        self.checkGroups("curve")
        # Handle postions of CVs for locator, joint, and geomety cases
        for obj in currentSelection:
            shapes = cmds.listRelatives(obj, shapes=True)
            if shapes:
                shapeTypes = [cmds.objectType(shape) for shape in shapes]
                if "locator" in shapeTypes:
                    locPos = cmds.pointPosition(obj)
                    objectPositions.append(locPos)
                else:
                    objPosition = cmds.xform(obj, query=True, worldSpace=True, translation=True)
                    objectPositions.append(objPosition)
            else:
                if cmds.objectType(obj) == "joint":
                    jointPos = cmds.xform(obj, query=True, worldSpace=True, translation=True)
                    objectPositions.append(jointPos)
        
        curveNumber = 0
        
        while True:
            curveName = f"ObjectCurve_{curveNumber}_Crv"
            if not cmds.objExists(curveName):
                objectCurve = cmds.curve(p=objectPositions, name = curveName)
                break
            else:
                curveNumber += 1

        cmds.parent(objectCurve, self.groupType)
        if cleanup:
            cmds.delete(currentSelection)

    # Creates a cluster at each CV of selected curve
    def clusterAtCV(self):
        selectedTransforms = cmds.ls(selection=True, type="transform")
        selectedCurve = None
        groupNumber = 0
        
        if len(selectedTransforms) != 1:
            openErrorWindow("Please select exactly 1 Nurbs curve.")
            raise ValueError("Please select exactly 1 curve.")

        for transform in selectedTransforms:
            if cmds.listRelatives(transform, type="nurbsCurve", children=True):
                selectedCurve = transform
                break

        # Get CVs of the selected curve
        curveCVs = cmds.ls(f'{selectedCurve}.cv[*]', flatten=True)

        if not curveCVs or len(curveCVs) < 4:
            openErrorWindow(f"A minimum of 4 CVs is needed on {selectedCurve}.")
            raise ValueError(f"A minimum of 4 CVs is needed on {selectedCurve}")

        # Create a cluster group
        while True:
            clusterGroupName = f"{selectedCurve}_{groupNumber}_Cluster_Grp"
            if not cmds.objExists(clusterGroupName):
                clusterGroup = cmds.group(empty=True, name = clusterGroupName)
                break
            else:
                groupNumber += 1

        self.checkGroups("cluster")

        cmds.parent(clusterGroup, self.groupType)

        # Create clusters for each CV and parent them to the cluster group
        for cv in curveCVs:
            curveCluster, handle = cmds.cluster(cv)
            cmds.parent(handle, clusterGroup)
    
    # Joint Tools Methods__________
    def jointsAtCVs(self):
        currentSelection = cmds.ls(selection=True, type="transform")
        selectedCurve = None
        
        if len(currentSelection) != 1:
            openErrorWindow("Select exactly 1 NURBS Curve.")
            raise ValueError("Select exactly 1 NURBS curve.")
        
        for transform in currentSelection:
            if cmds.listRelatives(transform, type="nurbsCurve", children=True):
                selectedCurve = transform
                break
        
        curveCVs = cmds.ls(f"{selectedCurve}.cv[*]", flatten=True)

        if not curveCVs:
            openErrorWindow(f"No CVs found on {selectedCurve}.")
            raise ValueError(f"No CVs on {selectedCurve}")
        
        self.checkGroups("joint")
        
        previousJoint = None
        chainNumber = 0
        groupNumber = 0

        while True:
            groupName = f"{selectedCurve}_{groupNumber}_Joint_Grp"
            if not cmds.objExists(groupName):
                jointGroup = cmds.group(empty=True, name=groupName)
                break
            else:
                groupNumber += 1

        for cv in curveCVs:
            cmds.select(clear=True)
            cvPosition = cmds.pointPosition(cv, world=True)
            while True:
                jointName = f"{selectedCurve}_{chainNumber}_Jnt"
                if not cmds.objExists(jointName):
                    currentJoint = cmds.joint(position = cvPosition, name=jointName)
                    break
                else:
                    chainNumber += 1                          
            
            if previousJoint:
                cmds.parent(currentJoint, previousJoint)
                cmds.joint(previousJoint, edit = True, zeroScaleOrient = True, orientJoint = self.jointOrientationChoice, secondaryAxisOrient = self.jointSecondaryChoice)

            previousJoint=currentJoint
        
        endJoint = cmds.ls(selection = True)
        rootJoint = endJoint
        
        while True:
            parentJoint = cmds.listRelatives(rootJoint, parent=True, type="joint")
            if parentJoint:
                rootJoint=parentJoint[0]
            else:
                break
        
        cmds.parent(rootJoint, jointGroup)

        cmds.parent(jointGroup, self.groupType)
    
    # Places a joint at the center of each selected object
    def jointsAtObjects(self):
        currentSelection = cmds.ls(selection=True, type="transform")
        if not currentSelection:
            openErrorWindow("Select at least one object to place joints.")
            raise ValueError("Select at least one object to place joints.")
        self.checkGroups("joint")
        previousJoint = None
        chainNumber = 0
        groupNumber = 0
        while True:
            groupName = f"JointChain_{groupNumber}_Joint_Grp"
            if not cmds.objExists(groupName):
                jointGroup = cmds.group(empty=True, name=groupName)
                break
            else:
                groupNumber += 1
        
        for obj in currentSelection:
            pos = cmds.xform(obj, query=True, worldSpace=True, translation=True)
            while True:
                jointName = f"jointChain_{groupNumber}_{chainNumber}_Jnt"
                if not cmds.objExists(jointName):
                    currentJoint = cmds.joint(position=(pos), name = jointName)
                    break
                else:
                    chainNumber += 1
            if previousJoint:
                cmds.joint(previousJoint, edit = True, zeroScaleOrient = True, orientJoint = self.jointOrientationChoice, secondaryAxisOrient = self.jointSecondaryChoice)
            
            previousJoint = currentJoint

        cmds.parent(jointGroup, self.groupType)
        cmds.select(clear=True)

    # Selects entire hierarchy of joints from anywhere within a joint chain
    def selectJointHierarchy(self):
        currentSelection = cmds.ls(selection=True, type = "joint")
        if currentSelection and len(currentSelection) == 1:
            endJoint = cmds.ls(selection = True)
            rootJoint = endJoint
        else:
            openErrorWindow("Select exactly 1 joint object.")
            raise ValueError("Select exactly 1 joint object")    
        
        while True:
            parentJoint = cmds.listRelatives(rootJoint, parent=True, type="joint")
            if parentJoint:
                rootJoint=parentJoint[0]
            else:
                break

        cmds.select(rootJoint)
        cmds.select(hierarchy=True)

    def setJointAxis(self):
        jointAxisIndex = self.jointAxisSelector.currentIndex()
        
        axisDictionary = {
            0 : "X",
            1 : "-X",
            2 : "Y",
            3 : "-Y",
            4 : "Z",
            5 : "-X",
        }

        self.jointAxisChoice = axisDictionary[jointAxisIndex]

    def setJointNumber(self):
        self.jointNumberChoice = int(self.jointNumberInput.text())

    def setJointSpacing(self):
        self.jointSpacingChoice = float(self.jointSpacingInput.text())

    def setJointOrientation(self):
        jointOrientationIndex = self.jointOrientationSelector.currentIndex()

        orientationDictionary = {
            0 : "xyz",
            1 : "yzx",
            2 : "zxy",
            3 : "zyx",
            4 : "yxz",
            5 : "xzy",
            6 : "none"
        }

        self.jointOrientationChoice = orientationDictionary[jointOrientationIndex]

    def setJointSecondary(self):
        jointSecondaryIndex = self.jointSecondarySelector.currentIndex()

        secondaryAxisDictionary = {
            0 : "xup",
            1 : "xdown",
            2 : "yup",
            3 : "ydown",
            4 : "zup",
            5 : "zdown",
        }

        self.jointSecondaryChoice = secondaryAxisDictionary[jointSecondaryIndex]

    # Creates a joint chain at the origin using values from joint creation UI
    def createJointChain(self, direction = "", number = 10, spacing = 1, jointOrient = "xyz", secondAxis = "yup"):

        self.setJointAxis()
        self.setJointNumber()
        self.setJointSpacing()
        self.setJointOrientation()
        self.setJointSecondary()

        direction = self.jointAxisChoice
        number = self.jointNumberChoice
        spacing = self.jointSpacingChoice
        jointOrient = self.jointOrientationChoice
        secondAxis = self.jointSecondaryChoice

        axisDictionary = {
            "X": lambda i: (i * spacing, 0.0, 0.0),
            "-X": lambda i: (-i * spacing, 0.0, 0.0),
            "Y": lambda i: (0.0, i * spacing, 0.0),
            "-Y": lambda i: (0.0, -i * spacing, 0.0),
            "Z": lambda i: (0.0, 0.0, i * spacing),
            "-Z": lambda i: (0.0, 0.0, -i * spacing),
        }

        self.checkGroups("joint")

        previousJoint = None
        chainNumber = 0
        groupNumber = 0
        # create a uniquely named group for this joint chain
        while True:
            groupName = f"JointChain_{groupNumber}_Joint_Grp"
            if not cmds.objExists(groupName):
                jointGroup = cmds.group(empty=True, name=groupName)
                break
            else:
                groupNumber += 1
        
        for i in range(number):
            if i == 0:
                currentJoint = cmds.joint(position=(0, 0, 0), name=f"jointChain_{groupNumber}_{chainNumber}_Jnt")
            else:
                jointPosition = axisDictionary[direction](i)
                while True:
                    jointName = f"jointChain_{groupNumber}_{chainNumber}_Jnt"
                    if not cmds.objExists(jointName):
                        currentJoint = cmds.joint(position=jointPosition, name=jointName)
                        cmds.joint(previousJoint, edit=True, zeroScaleOrient=True, orientJoint=jointOrient, secondaryAxisOrient=secondAxis)
                        break
                    else:
                        chainNumber += 1
                
            previousJoint = currentJoint

        cmds.parent(jointGroup, self.groupType)

        cmds.select(clear=True)

    def resetJointTools(self):
        self.jointAxisSelector.setCurrentIndex(0)
        self.jointNumberInput.setText("10")
        self.jointNumberChoice = 10
        self.jointSpacingInput.setText("1.0000")
        self.jointSpacingChoice = 1.0000
        self.jointOrientationSelector.setCurrentIndex(0)
        self.jointOrientationChoice = "xyz"
        self.jointSecondarySelector.setCurrentIndex(2)
        self.jointSecondaryChoice = "yup"

    # Constraint Tools Methods_____________________
    def setTransformConstraintType(self, type):
        self.parentConstraintStatus = ""
        self.orientConstraintStatus = ""
        self.pointConstraintStatus = ""
        # Parent is checked. point and orient should be off
        if type == "parent" and self.createParentConstraintCheckbox.isChecked():
            self.createOrientConstraintCheckbox.setChecked(False)
            self.createPointConstraintCheckbox.setChecked(False)
            self.parentConstraintStatus = "parent"
            self.orientConstraintStatus = ""
            self.pointConstraintStatus = ""
        # point is checked. At least parent should be off
        elif type == "point" and self.createPointConstraintCheckbox.isChecked():
            self.createParentConstraintCheckbox.setChecked(False)
            self.parentConstraintStatus = ""
            self.pointConstraintStatus = "point"
            if self.createOrientConstraintCheckbox.isChecked():
                self.orientConstraintStatus = "orient"
            else:
                self.orientConstraintStatus = ""
        # orient is checked. At least parent should be off
        elif type == "orient" and self.createOrientConstraintCheckbox.isChecked():
            self.createParentConstraintCheckbox.setChecked(False)
            self.parentConstraintStatus = ""
            self.orientConstraintStatus = "orient"
            if self.createPointConstraintCheckbox.isChecked():
                self.pointConstraintStatus = "point"
            else:
                self.pointConstraintStatus = ""

        self.parentConstraintChoice = self.parentConstraintStatus
        self.pointConstraintChoice = self.pointConstraintStatus
        self.orientConstraintChoice = self.orientConstraintStatus

    def setScaleConstraint(self):
        if self.createScaleConstraintCheckbox.isChecked():
            self.scaleConstraintChoice = "scale"
        else:
            self.scaleConstraintChoice = ""

    def setMaintainOffset(self):
        self.maintainOffsetChoice = self.constraintOffsetCheckbox.isChecked()

    def setAllowMultipleConstraints(self):
        self.allowMultipleConstraintsChoice = self.constraintAllowMultipleCheckbox.isChecked()

    def processSelection(self):
        self.transformsArray = cmds.ls(selection=True, type="transform")

        if not self.transformsArray:
            #print("Please select a minimum of one transfrom node")
            openErrorWindow("Please select a minimum of one transform node.")
            raise ValueError("Please select a minimum of one transfrom node")
        
        # If creating constraints, the first object selected will always be the parent
        self.constraintParent = self.transformsArray[0]

        # In the case only one object with constraints will be baked
        remainingTransforms = self.transformsArray[1:] if len(self.transformsArray) > 1 else []

        # If baking for AE, We only want locators to work
        self.locatorsArray = [
            transform for transform in remainingTransforms
            if cmds.listRelatives(transform, type="locator", children=True)
        ]

        # Any object that will be constrained
        self.childArray = [
            transform for transform in remainingTransforms
        ]
        
        # Create a list of all constraints associated with the transforms in transformsArray
        # They are separated by category to control what channels are eventually baked
        self.parentConstraintArray = [
            relative for x in self.transformsArray
            for relative in cmds.listRelatives(x) or []
            if cmds.objectType(relative, isType="parentConstraint")
        ]

        self.pointConstraintArray = [
            relative for x in self.transformsArray
            for relative in cmds.listRelatives(x) or []
            if cmds.objectType(relative, isType="pointConstraint")
        ]

        self.scaleConstraintArray = [
            relative for x in self.transformsArray
            for relative in cmds.listRelatives(x) or []
            if cmds.objectType(relative, isType="scaleConstraint")
        ]

        # Any selected transform that already has a constraint gets added to the constrainedObjectArray
        self.constrainedObjectArray = [
            x for x in self.transformsArray
            if any(
                cmds.objectType(relative, isType="parentConstraint") or
                cmds.objectType(relative, isType="scaleConstraint") or
                cmds.objectType(relative, isType="pointConstraint")
                for relative in cmds.listRelatives(x) or []
            )
        ]

    def createMultipleConstraints(self):
        self.processSelection()

        incomingTypes = [self.parentConstraintChoice, self.pointConstraintChoice, self.orientConstraintChoice, self.scaleConstraintChoice]

        # Protect against no constraint types being checked
        if all(t == '' for t in incomingTypes):
            openErrorWindow("Please select a minimum of 1 constraint type.")
            raise ValueError("Please select a minimum of one constraint type")
        
        # Filter out empty types
        types = [t for t in incomingTypes if t]
        
        offset = self.maintainOffsetChoice
        print(f"types: {types}")
        if not isinstance(types, list):
            types = types

        if not len(self.transformsArray) > 1:
            openErrorWindow("A minimum of 2 transforms must be selected.")
            raise ValueError("A minimum of two tranforms must be selected.")

        # Prevent the user from applying a constraint to an object that is already directly animated
        animatedChildren = [
            x for x in self.childArray
            if cmds.keyframe(x, query=True, keyframeCount = True)
        ]

        if animatedChildren:
            raise ValueError(
                f"The following objects have animation applied: {', '.join(animatedChildren)}. \n"
                f"It is against best practice to constrain animated objects. \n"
                f"use buffer groups if animation is needed."
            )
        
        # Prevent both parent and point constraints from being applied simultaneously
        # should be prevented via UI, but ya never know
        if "parent" in types and "point" in types:
            openErrorWindow("Cannot apply both parent and point constraints simultaneously.")
            raise ValueError("Cannot apply both parent and point constraints simultaneously.")
        
        elif "parent" in types and "orient" in types:
            openErrorWindow("Cannot apply both parent and orient constraints simultaneously.")
            raise ValueError("Cannot apply both parent and orient constraints simultaneously.")

        # Check for existing constraints
        if not self.allowMultipleConstraintsChoice: #allow multiple constraints if box is checked
            for child in self.childArray:
                existingConstraints = cmds.listRelatives(child, type="constraint") or []
                existingConstraintsTypes = set(cmds.nodeType(c) for c in existingConstraints)

                # Prevent duplicate and conflicting constraints
                if "parent" in types:
                    if "parentConstraint" in existingConstraintsTypes:
                        openErrorWindow(f"Parent constraint already exists on {child}.")
                        raise ValueError(f"Parent constraint already exists on {child}.")
                    if "pointConstraint" in existingConstraintsTypes:
                        openErrorWindow(f"Cannot add a parent constraint to {child} as it already has a point constraint.")
                        raise ValueError(f"Cannot add a parent constraint to {child} as it already has a point constraint.")
                    if "orientConstraint" in existingConstraintsTypes:
                        openErrorWindow(f"Cannot add a parent constraint to {child} as it already has an orient constraint.")
                        raise ValueError(f"Cannot add a parent constraint to {child} as it already has an orient constraint.")

                if "point" in types:
                    if "pointConstraint" in existingConstraintsTypes:
                        openErrorWindow(f"Point constraint already exists on {child}.")
                        raise ValueError(f"Point constraint already exists on {child}.")
                    if "parentConstraint" in existingConstraintsTypes:
                        openErrorWindow(f"Cannot add a point constraint to {child} as it already has a parent constraint.")
                        raise ValueError(f"Cannot add a point constraint to {child} as it already has a parent constraint.")
                    
                if "orient" in types:
                    if "orientConstraint" in existingConstraintsTypes:
                        openErrorWindow(f"Orient constraint already exists on {child}.")
                        raise ValueError(f"Orient constraint already exists on {child}.")
                    if "parentConstraint" in existingConstraintsTypes:
                        openErrorWindow(f"Cannot add an orient constraint to {child} as it already has a parent constraint.")
                        raise ValueError(f"Cannot add an orient constraint to {child} as it already has a parent constraint.")

                if "scale" in types and "scaleConstraint" in existingConstraintsTypes:
                    openErrorWindow(f"Scale constraint already exists on {child}.")
                    raise ValueError(f"Scale constraint already exists on {child}.")


        constraintCommands = {
            "parent": cmds.parentConstraint,
            "point": cmds.pointConstraint,
            "orient": cmds.orientConstraint,
            "scale": cmds.scaleConstraint,
        }

        # Create specified constraints and place all the constraints into the self.constraintArray
        for constraintType in types:
            if constraintType in constraintCommands:
                constraintFunc = constraintCommands[constraintType]
                self.constraintArray.extend(
                    constraintFunc(self.constraintParent, child, maintainOffset=offset)[0]
                    for child in self.childArray
                )
            else:
                openErrorWindow(f"Unsupported constraint type: {constraintType}.")
                raise ValueError(f"Unsupported constraint type: {constraintType}")
    
    def getAnimationStart(self):
        animStart = cmds.playbackOptions(query=True, animationStartTime=True)
        self.bakeConstraintsStartInput.setText(str(animStart))

    def getPlaybackStart(self):
        playbackStart = cmds.playbackOptions(query=True, minTime=True)
        self.bakeConstraintsStartInput.setText(str(playbackStart))

    def getAnimationEnd(self):
        animEnd = cmds.playbackOptions(query=True, animationEndTime=True)
        self.bakeConstraintsEndInput.setText(str(animEnd))

    def getPlaybackEnd(self):
        playbackEnd = cmds.playbackOptions(query=True, maxTime=True)
        self.bakeConstraintsEndInput.setText(str(playbackEnd))

    def setBakeStart(self):
        if not self.bakeConstraintsStartInput.text() == "":
            self.bakeStart = float(self.bakeConstraintsStartInput.text())
            return self.bakeStart
        else:
            openErrorWindow("Bake Start Time not set")
            raise ValueError("Please select a start time for baking")
        
    def setBakeEnd(self):
        if not self.bakeConstraintsEndInput.text() == "":
            self.bakeEnd = float(self.bakeConstraintsEndInput.text())
            return self.bakeEnd
        else:
            openErrorWindow("Bake End Time not set")
            raise ValueError("Please select an end time for baking")

    def bakeConstraints(self):
        self.processSelection()
        if not self.constrainedObjectArray:
            openErrorWindow("No selected objects contain constraints.")
            raise ValueError("No selected objects contain constraints")
        
        # Only bake channels that are constrained
        attributesToBake = set()
        if self.parentConstraintArray:
            attributesToBake.update(["tx", "ty", "tz", "rx", "ry", "rz"])
        if self.pointConstraintArray:
            attributesToBake.update(["tx", "ty", "tz"])
        if self.scaleConstraintArray:
            attributesToBake.update(["sx", "sy", "sz"])

        if attributesToBake:
            bakeStart = self.setBakeStart()
            bakeEnd = self.setBakeEnd()
            cmds.bakeResults(
                self.constrainedObjectArray,
                t=(bakeStart, bakeEnd),
                sampleBy=1,
                attribute=list(attributesToBake),
                preserveOutsideKeys=True
            )
    
    def cleanupBakedConstraints(self):
        constraintsToDelete = (
            self.parentConstraintArray +
            self.pointConstraintArray +
            self.scaleConstraintArray
        )
        
        if constraintsToDelete:
            cmds.delete(constraintsToDelete)

    def convertConstraintsToAnim(self):
        self.bakeConstraints()
        self.cleanupBakedConstraints()

    def createAEConstraints(self):
        self.processSelection()
        if not len(self.transformsArray) > 1:
            openErrorWindow("A minimum of one transform and one locator must be selected.")
            raise ValueError("A minimum of one tranform and one locator must be selected")
        if not self.locatorsArray:
            openErrorWindow("No locators were found in selection.")
            raise ValueError("No locators were found in selection")
        
        # Parent Constrain all selected locators to the first selection
        self.AEParentConstraints = [
            cmds.parentConstraint(self.constraintParent, child, maintainOffset=True)[0]
            for child in self.locatorsArray
        ]

        # Make sure any scale animation is also accounted for
        self.AEScaleConstraints = [
            cmds.scaleConstraint(self.constraintParent, child, maintainOffset=True)[0]
            for child in self.locatorsArray
        ]

    def bakeAEConstraints(self):
        bakeStart = self.setBakeStart()
        bakeEnd = self.setBakeEnd()
        cmds.bakeResults(
            self.locatorsArray,
            t=(bakeStart, bakeEnd),
            sampleBy=1,
            attribute=["tx", "ty", "tz"],
            preserveOutsideKeys=True
        )

    def cleanupAEConstraints(self):
        constraintsToDelete = (
            self.AEParentConstraints +
            self.AEScaleConstraints
        )

        if constraintsToDelete:
            cmds.delete(constraintsToDelete)

    def bakeLocatorsForAE(self):
        self.createAEConstraints()
        self.bakeAEConstraints()
        self.cleanupAEConstraints()

    def findConstraintParent(self):
        self.constraintParents.clear()
        currentSelection = cmds.ls(selection=True)
        
        # Ensure only one object is selected
        if len(currentSelection) != 1:
            self.constraintParentsInput.setText("Select exactly 1 object")
            openErrorWindow("Please select exactly 1 object to search.")
            raise ValueError("Please select exactly 1 object to search")
        
        getFirst = currentSelection[0]
        
        # Helper function to find and add parent objects
        def addParentObjects(obj):
            parentObjects = cmds.listConnections(obj + ".target", source=True)
            if parentObjects:
                for target in parentObjects:
                    if target != obj:
                        self.constraintParents.add(target)

        # Check if the object itself is a constraint
        if cmds.ls(getFirst, type="constraint"):
            addParentObjects(getFirst)

        # Check for constraints applied to the object
        constraints = cmds.listRelatives(getFirst, type="constraint")
        if not constraints and not cmds.ls(getFirst, type="constraint"):
            self.constraintParentsInput.setText("No constraint parents")
            openErrorWindow(f"{getFirst} is not a constrained child.")
            raise ValueError(f"{getFirst} is not a constrained child.")
        
        # Process each constraint found
        if constraints:
            for constraint in constraints:
                addParentObjects(constraint)

        # Update UI with constraint parent results if any
        if self.constraintParents:
            self.constraintParentsInput.setText(str(list(self.constraintParents)))

    def selectConstraintParents(self):
        self.findConstraintParent()
        if self.constraintParents:
            cmds.select(self.constraintParents)
            self.constraintParentsInput.setText("")
        else:
            self.constraintParentsInput.setText("Nothing to select")

    def findConstraintChildren(self):
        self.constraintChildren.clear()
        currentSelection = cmds.ls(selection=True)
        if len(currentSelection) != 1:
            self.constraintChildrenInput.setText("Select exactly 1 object")
            openErrorWindow("Please select exactly 1 object to search.")
            raise ValueError("Please select exactly 1 object to search")
        getFirst = currentSelection[0]
        constraints = cmds.listConnections(getFirst, type="constraint", source=False, destination=True)
        if not constraints:
            self.constraintChildrenInput.setText("No constrained children")
            openErrorWindow(f"{getFirst} does not have constrained children.")
            raise ValueError(f"{getFirst} does not have constrained children.")
        for constraint in constraints:
            childrenObjects = cmds.listConnections(constraint + ".constraintParentInverseMatrix", destination=True)
            if childrenObjects:
                for obj in childrenObjects:
                    if obj != getFirst:
                        self.constraintChildren.add(obj)
            else:
                self.constraintChildrenInput.setText("none")
                openErrorWindow(f"{getFirst} is not is not the constraint parent of any objects.")
                raise ValueError(f"{getFirst} is not the constraint parent of any objects")
        
        if self.constraintChildren:
            self.constraintChildrenInput.setText(str(list(self.constraintChildren)))
        else:
            self.constraintChildrenInput.setText("none")
            openErrorWindow(f"{getFirst} is not the constraint parent of any objects.")
            raise ValueError(f"{getFirst} is not the constraint parent of any objects")
        
    def selectConstraintChildren(self):
        self.findConstraintChildren()
        if self.constraintChildren:
            cmds.select(self.constraintChildren)
            self.constraintChildrenInput.setText("")
        else:
            self.constraintChildrenInput.setText("Nothing to select")

    def getSceneInfo(self):
        info = []
        application = cmds.fileInfo("application", query=True)
        version = cmds.fileInfo("version", query=True)
        product = cmds.fileInfo("product", query=True)
        OSVersion = cmds.fileInfo("osv", query=True)
        cutID = cmds.fileInfo("cutIdentifier", query=True)
        
        info.append(application)
        info.append(version)
        info.append(product)
        info.append(cutID)
        info.append(OSVersion)

        checkForEntries = [i for i in info if i]
        if checkForEntries:
            self.sceneApplicationFeedback.setText(application[0])
            self.sceneVersionFeedback.setText(version[0])
            self.sceneProductFeedback.setText(product[0])
            self.sceneOSVersionFeedback.setText(OSVersion[0])
            self.sceneCutFeedback.setText(cutID[0])
        else:
            self.sceneApplicationFeedback.setText("unsaved scene")
            self.sceneVersionFeedback.setText("unsaved scene")
            self.sceneProductFeedback.setText("unsaved scene")
            self.sceneOSVersionFeedback.setText("unsaved scene")
            self.sceneCutFeedback.setText("unsaved scene")

    # Handles scene group creations and parenting 
    def checkGroups(self, mode):
        sceneDeformersGroup = "Deformers_Grp"
        
        modeDictionary = {
            "locator": "VertexLocators_Grp",
            "curve": "Curves_Grp",
            "control": "Controls_Grp",
            "cluster": "Clusters_Grp",
            "joint": "Joints_Grp"
        }

        if mode in modeDictionary:
            groupName = modeDictionary[mode]
            if not cmds.objExists(groupName):
                self.groupType = cmds.group(empty=True, name=groupName)
            else:
                self.groupType = groupName
            
        if cmds.objExists(sceneDeformersGroup):
            self.deformersGroup = sceneDeformersGroup
            children = cmds.listRelatives(self.deformersGroup, children=True) or []
            if self.groupType not in children:
                cmds.parent(self.groupType, self.deformersGroup)
        else:
            cmds.warning("Deformers_Grp does not exist. Check project settings.")

class HybridToolboxErrorGUI(QtWidgets.QMainWindow):
    def __init__(self, windowName, errorMessage, parent = None):
        super().__init__(parent)
        self.setObjectName(windowName)
        self.setMinimumWidth(400)
        self.message = errorMessage
        
        # On macOS make window a Tool to keep it on top of Maya
        if sys.platform == "darwin":
            self.setWindowFlag(QtCore.Qt.Tool, True)

        self.errorBaseWindow = QtWidgets.QWidget()
        self.setWindowTitle(windowName)
        self.setCentralWidget(self.errorBaseWindow)

        self.errorLayout = QtWidgets.QHBoxLayout()
        self.errorBaseWindow.setLayout(self.errorLayout)

        self.errorMessageText = QtWidgets.QLabel(self.message)
        self.errorLayout.addWidget(self.errorMessageText)
        self.move(500,200)
        self.show()

def checkWindow(qtObjectName):
    if cmds.window(qtObjectName, exists=True):
        cmds.deleteUI(qtObjectName, wnd=True)

def getMayaMain():
    winPoint = MQtUtil.mainWindow()
    return wrapInstance(int(winPoint), QtWidgets.QWidget)

def openWindow():
    windowName = "Hybrid Toolbox v1.5.71 Dev"
    checkWindow(windowName)
    HybridToolbox = HybridToolboxGUI(windowName, getMayaMain())

def openErrorWindow(message):
    windowName = "Hybrid Toolbox error"
    errorMessage = message
    checkWindow(windowName)
    HybridtoolboxErrorWindow = HybridToolboxErrorGUI(windowName, errorMessage, getMayaMain())