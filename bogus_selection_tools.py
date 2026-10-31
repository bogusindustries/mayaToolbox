"""
bogus_selection_tools.py
Selection tools for Maya.
"""
import maya.cmds as cmds

class BogusSelectionTools:

    def selection_count(self):
        return len(cmds.ls(selection=True))
    
    def selectHierarchy(self):
        currentSelection = cmds.ls(selection=True)
        if not currentSelection:
            cmds.warning("Select an object.")
            return
        cmds.select(currentSelection, hierarchy=True)

    def findRoot(self):
        currentSelection = cmds.ls(selection=True)
        if not currentSelection:
            cmds.warning("Select an object.")
            return
        root = cmds.listRelatives(currentSelection, parent=True, fullPath=True)
        cmds.select(root)

    def findHighestRoot(self):
        currentSelection = cmds.ls(selection=True)
        if not currentSelection:
            cmds.warning("Select an object.")
            return
        root = currentSelection
        while root:
            parent = cmds.listRelatives(root, parent=True, fullPath=True)
            if not parent:
                break
            root = parent
        cmds.select(root)

    def selectAllByType(self, nodeType):
        target = cmds.ls(type=nodeType, noIntermediate=True, long=True) or[]
        if not target:
            print(f"No {nodeType} nodes found.")
            return
        if nodeType != "animCurve":
            transforms = list(set(cmds.listRelatives(target, parent=True, fullPath=True) or []))
            cmds.select(transforms, replace=True)

        if nodeType == "joint":
            cmds.select(clear=True)
            visitedJoints = set()
            for joint in target:
                rootJoint = joint

                while True:
                    parentJoint = cmds.listRelatives(rootJoint, parent=True, type="joint")
                    if parentJoint:
                        rootJoint = parentJoint[0]
                    else:
                        break

                if rootJoint not in visitedJoints:
                    cmds.select(rootJoint, add=True)
                    visitedJoints.add(rootJoint)
        
        else:
            cmds.select(target, replace=True)

    def selectAllAnimatedObjects(self):
        curves = cmds.ls(type="animCurve") or []
        if not curves:
            return
        plugs = cmds.listConnections(curves, source=False, destination=True, plugs=True, skipConversionNodes=True) or []
        connected = cmds.listConnections(curves, source=False, destination=True, skipConversionNodes=True) or []
        drivenObjects = cmds.ls(connected, dag=True, long=True) or []
        transforms = set()
        for node in drivenObjects:
            if cmds.objectType(node, isAType="transform"):
                transforms.add(node)
            else:
                transforms.update(cmds.listRelatives(node, parent=True, fullPath=True) or [])
        cmds.select(list(transforms), replace=True)

