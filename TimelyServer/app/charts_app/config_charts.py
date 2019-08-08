from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

__slots__ = ['Config_Charts']

class Config_Charts:
    chose_colors = (
        colors.ReportLabBlueOLD, colors.ReportLabBlue, colors.ReportLabBluePCMYK, colors.ReportLabLightBlue,
        colors.ReportLabFidBlue, colors.ReportLabFidRed, colors.ReportLabGreen, colors.ReportLabLightGreen,
        colors.aliceblue, colors.aqua, colors.aquamarine, colors.azure, colors.beige,
        colors.bisque, colors.black, colors.blanchedalmond, colors.blue, colors.blueviolet, colors.brown,
        colors.burlywood, colors.cadetblue, colors.chartreuse, colors.chocolate, colors.coral, colors.cornflowerblue,
        colors.cornsilk, colors.crimson, colors.cyan, colors.darkblue, colors.darkcyan, colors.darkgoldenrod,
        colors.darkgray, colors.darkgrey, colors.darkgreen, colors.darkkhaki, colors.darkmagenta, colors.darkolivegreen,
        colors.darkorange, colors.darkorchid, colors.darkred, colors.darksalmon, colors.darkseagreen, colors.darkslateblue,
        colors.darkslategray, colors.darkslategrey, colors.darkturquoise, colors.darkviolet, colors.deeppink,
        colors.deepskyblue, colors.dimgray, colors.dimgrey, colors.dodgerblue, colors.firebrick,
        colors.forestgreen, colors.fuchsia, colors.gainsboro, colors.gold, colors.goldenrod,
        colors.gray, colors.green, colors.greenyellow, colors.honeydew, colors.hotpink, colors.indianred, colors.indigo,
        colors.ivory, colors.khaki, colors.lavender, colors.lavenderblush, colors.lawngreen, colors.lemonchiffon,
        colors.lightblue, colors.lightcoral, colors.lightcyan, colors.lightgoldenrodyellow, colors.lightgreen,
        colors.lightgrey, colors.lightpink, colors.lightsalmon, colors.lightseagreen, colors.lightskyblue,
        colors.lightslategray, colors.lightsteelblue, colors.lightyellow, colors.lime, colors.limegreen, colors.linen,
        colors.magenta, colors.maroon, colors.mediumaquamarine, colors.mediumblue, colors.mediumorchid, colors.mediumpurple,
        colors.mediumseagreen, colors.mediumslateblue, colors.mediumspringgreen, colors.mediumturquoise,
        colors.mediumvioletred, colors.midnightblue, colors.mintcream, colors.mistyrose, colors.moccasin,
        colors.navy, colors.oldlace, colors.olive, colors.olivedrab, colors.orange, colors.orangered,
        colors.orchid, colors.palegoldenrod, colors.palegreen, colors.paleturquoise, colors.palevioletred,
        colors.papayawhip, colors.peachpuff, colors.peru, colors.pink, colors.plum, colors.powderblue, colors.purple,
        colors.red, colors.rosybrown, colors.royalblue, colors.saddlebrown, colors.salmon, colors.sandybrown,
        colors.seagreen, colors.seashell, colors.sienna, colors.silver, colors.skyblue, colors.slateblue,
        colors.slategray, colors.slategrey, colors.snow, colors.springgreen, colors.steelblue, colors.tan, colors.teal,
        colors.thistle, colors.tomato, colors.turquoise, colors.violet, colors.wheat,
        colors.yellow, colors.yellowgreen, colors.fidblue, colors.fidred, colors.fidlightblue,
    )
    pagesize = A4
    typeface = 'SimSun'
    # typefacefile = '../../SimSun.ttf'
    typefacefile = 'SimSun.ttf'
    showname = ('统计日期', '访问次数', '扫码次数', '验伪次数')