from Acquisition import aq_base
from plone import api


default_profile = "collective.volto.enhancedlinks:default"


def cleanup_memojito_on_object(obj, path, **kwargs):
    obj = aq_base(obj)
    if hasattr(obj, "_memojito_"):
        if [k for k in obj._memojito_ if k[0] == "get_enhanced_infos"]:
            obj._memojito_ = {
                k: v for k, v in obj._memojito_.items() if k[0] != "get_enhanced_infos"
            }
        # del obj.memojito


def cleanup_memojito(context):
    catalog = api.portal.get_tool(name="portal_catalog")
    portal = api.portal.get()
    catalog.ZopeFindAndApply(
        portal,
        apply_func=cleanup_memojito_on_object,
        apply_path="/".join(portal.getPhysicalPath()),
    )


def to_1001(context):
    setup_tool = api.portal.get_tool(name="portal_setup")
    setup_tool.runImportStepFromProfile(default_profile, "toolset")
    cleanup_memojito(context)
