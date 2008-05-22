#-!-coding: utf-8 -!-

from django.shortcuts import render_to_response

from django.utils.translation import ugettext as _

import dms.settings
import copy

from dms.roles          import require_permission
from dms.utils_form     import get_item_vars_show
from dms.queries        import get_top_item_container
from dms.queries        import get_site_by_id

@require_permission('perm_manage_site')
def generate_my_css_data(request, save_css):
  """ Erzeugt die entsprechenden Stylesheets """
  v = {}
  nFontSize = 4
  # --- linker Rand fuer Schmuckbild
  site = get_site_by_id(1)
  if site.left_image_url == '':
    v['left_image_margin'] = '0'
    v['left_margin'] = 212 - 30
  else:
    v['left_image_margin'] = '30'
    v['left_margin'] = 212

  name = 'standard'
  v['rgbBodyBg']          = '#000092'
  v['nFontSize']          = 4

  v['nWidth']             = 190
  v['nWidth_05']          = 190 + 5
  v['nWidth_10']          = 190 - 10
  v['nHeight']            = 200
  v['nTopLeft']           = 20
  v['nTopTop']            = 12
  v['nTopMain']           = 132
  v['nTopMain_28']        = v['nTopMain'] + 28
  v['nTopMain_30']        = v['nTopMain'] + 30
  v['nTopMain_36']        = v['nTopMain'] + 36
  v['nTopMain_42']        = v['nTopMain'] + 42
  v['nTopMain_60']        = v['nTopMain'] + 60
  v['nTopMain_026']       = v['nTopMain'] - 26
  v['nTopHeight']         = 30
  v['nWidthExt']          = 220
  v['nWidthExt_2']        = 110
  v['nWidthExt_4']        = 220 + 4
  v['nMarginLeft']        = 0
  v['nMarginRight']       = 0
  v['nLInfoBorderWidth']  = 1
  v['nRInfoBorderWidth']  = 1
  v['nLFrameBorderWidth'] = 1
  v['nRFrameBorderWidth'] = 1
  v['nLFrameWidth']       = 1
  v['nRFrameWidth']       = 1
  v['cLFrameStyle']       = 'dotted'
  v['cRFrameStyle']       = 'dashed'
  v['nFooterTop']         = 10
  v['nFooterTop_2']       = 5
  v['nFooterTop_3']       = 3
  v['nFooterWidth']       = 1
  v['cFooterStyle']       = 'none'
  v['cTextDecoration']    = 'none'
  v['cBaseFont']          = 'font-family: Lucida, Verdana, Arial, Helvetica, sans-serif'
  v['arrSize_04']         = '72%'
  v['arrSize_03']         = '72%'
  v['arrSize_02']         = '80%'
  v['arrSize_01']         = '90%'
  v['arrSize']            = '100%'
  v['arrSize_1']          = '120%'
  v['arrSize_2']          = '160%'
  v['arrSize_3']          = '180%'
  v['arrSize_4']          = '240%'
  v['arrSize_5']          = '240%'
  v['arrSize_6']          = '240%'
  v['arrSize_7']          = '240%'
  v['rgbRot']             = '#be564a'
  v['rgbDarkBg']          = '#3492b2'
  v['rgbLightBg']         = '#bad8e3'
  v['rgbFrameBg']         = '#f4f4f8'
  v['rgbFrameBg']         = '#fff'
  v['rgbSelectBlock']     = '#f0f0f8'

  v['rgbSearchBg']        = v['rgbDarkBg']
  v['rgbBreadcumb']       = '#e0e0fc'
  v['rgbBreadcumbBg']     = v['rgbLightBg']
  v['rgbANavTopLink']     = '#fff'
  v['rgbAHoverTopBg']     = v['rgbLightBg']
  v['rgbFrameHeaderBg']   = v['rgbFrameBg']

  v['rgbLightGrey']       = '#c0c0c0'
  v['rgbGrey']            = '#a0a0a0'
  v['rgbDarkGrey']       = '#808080'
  v['rgbHeadLine']        = '#1F669D'
  v['rgbHead']            = '#203090'
  v['rgbHead2']           = '#cc0000'
  v['rgbHead3']           = v['rgbDarkGrey']
  v['rgbHeaderSymBg']     = '#cc0000'
  v['rgbFrameBorder']     = '#d0d0f0'
  v['rgbHeaderBlock']     = '#e5e5e5'
  v['rgbIntroBlock']      = '#e8e8ed'
  v['rgbLightHeaderBg']   = '#e0e0f0'
  v['rgbToDoBg']          = '#8080a0'
  v['rgbLightToDoBg']     = '#b0b0d0'
  v['rgbPortalTabBg']     = '#606080'
  v['rgbNavigationBg']    = '#f4f4f4'
  v['rgbFrameBlock']      = '#f0f0ff'
  v['rgbWhite']           = '#fff'
  v['rgbBlack']           = '#000'
  v['rgbRed']             = 'red'
  v['rgbBlue']            = 'blue'
  v['rgbDarkBlue']        = '#000080'
  v['rgbAttention']       = v['rgbRed']

  v['rgbTabHeaderBg']       = v['rgbLightBg']
  v['rgbTabHeaderBgExt']    = v['rgbDarkBg']
  v['rgbTabHeaderText']     = '#080683'
  v['rgbFrameHeaderText']   = v['rgbHead']
  v['rgbAdminHeaderText']   = v['rgbGrey']

  v['rgbMarginBlock']     = '#606080'
  v['rgbHeaderSym']       = v['rgbBlack']
  v['rgbFrameSymBg']      = v['rgbHead']
  v['rgbAdminSymBg']      = v['rgbGrey']
  v['rgbExtLink']         = v['rgbRed']
  v['rgbPNavigate']       = '#606060'
  v['rgbNaviOn']          = '#CF2431'

  v['rgbANormal']         = '#715d9b'
  v['rgbAextended']       = '#b01010'
  v['rgbAPortalLink']     = v['rgbANormal']
  v['rgbAFrameLink']      = v['rgbAPortalLink']
  v['rgbANav']            = v['rgbAPortalLink']
  v['rgbACommandNav']     = '#9b5d71'
  v['rgbACommandNav']     = '#715d9b'
  v['rgbANavLink']        = v['rgbAPortalLink']
  v['rgbANavHeadLink']    = v['rgbAPortalLink']
  v['rgbAHeadInfo']       = '#8060a0'
  v['rgbAOverlay']        = v['rgbANormal']
  v['rgbAMainLink']       = '#8080c0'
  v['rgbAMainLink']       = '#194757'
  v['rgbACommandLink']    = '#903020'
  v['rgbASubLink']        = '#a04040'
  v['rgbASubLink']        = '#8080c0'
  v['rgbA']               = '#715d9b'
  v['rgbA']               = '#880000'
  v['rgbABg']             = v['rgbSelectBlock']
  v['rgbAActive']         = v['rgbRed']
  v['rgbAActiveBg']       = '#F0F0F4'
  v['rgbANo_hightlight']  = v['rgbWhite']
  v['rgbHighlightOn']     = v['rgbAMainLink']
  v['rgbHighlightOff']    = v['rgbWhite']
  v['rgbFrameHighlightOn'] = v['rgbACommandLink']
  v['rgbCaptionBg']       = '#3e48a0'
  v['rgbCaptionText']     = v['rgbWhite']

  v['rgbAHoverBg']        = v['rgbDarkBg']
  v['rgbAHover']          = v['rgbWhite']
  v['rgbACommandHoverBg'] = v['rgbFrameHighlightOn']
  v['rgbACommandHover']   = v['rgbWhite']

  v['rgbInput']           = v['rgbDarkBg']
  v['rgbInputSubmitBorder'] = v['rgbInput']
  v['rgbInputSubmitColor']  = v['rgbWhite']
  v['rgbInputSubmitBg']   = v['rgbCaptionBg']
  v['rgbInputCheckboxBg'] = '#f8f8fa'
  v['rgbOptionBorder']    = v['rgbInputSubmitBorder']
  v['rgbOptionBg']        = v['rgbInputCheckboxBg']
  v['rgbTextareaBorder']  = v['rgbDarkBg']
  v['rgbTextareaBg']      = v['rgbWhite']
  v['rgbBorderTopLeft']   = '#acaecc'
  v['rgbBorderTopLeft']   = '#ddddee'
  v['rgbBorderBottomRight'] = '#acaecc'
  v['rgbBorderBg']        = v['rgbWhite']
  v['rgbBorderedTable']   = v['rgbBorderTopLeft']
  v['rgbInfoBorder']      = '#f0f0ff'
  v['rgbLFrameBorder']    = v['rgbFrameBorder']
  v['rgbRFrameBorder']    = '#8080a0'
  v['rgbFooterColor']     = '#d0d0ef'

  v['rgbBody']            = v['rgbBlack']
  v['rgbBodyBg']          = v['rgbWhite']
  va = copy.copy ( v )
  save_css ( name, va )

  name = 'afl'
  va = v
  va['rgbDarkBg']         = '#3492b2'
  va['rgbLightBg']        = '#bad8e3'
  va['rgbTabHeaderBgExt'] = va['rgbDarkBg']
  va['rgbFrameBg']        = '#f4f4f8'
  va['rgbSelectBlock']    = '#f0f0f8'
  va['rgbSearchBg']       = va['rgbDarkBg']
  va['rgbBreadcumb']      = '#e0e0fc'
  va['rgbBreadcumbBg']    = va['rgbLightBg']
  va['rgbANavTopLink']    = '#fff'
  va['rgbAHoverTopBg']    = va['rgbLightBg']
  va['rgbAHoverBg']       = va['rgbDarkBg']
  va['rgbANavTopLink']    = '#fff'
  va['rgbAHoverTopBg']    = va['rgbLightBg']
  va['rgbTabHeaderBg']     = va['rgbLightBg']
  va['rgbTabHeaderText']   = '#080683'
  va['rgbFrameBorder']     = va['rgbDarkBg']
  va['rgbFrameHeaderBg']   = va['rgbLightBg']
  save_css ( name, va )

  name = 'bs'
  va = copy.copy ( v )
  va['rgbDarkBg']          = '#888890'
  va['rgbLightBg']         = '#e2e2f0'
  va['rgbTabHeaderBgExt']  = va['rgbDarkBg']
  va['rgbFrameBg']         = '#f4f4f8'
  va['rgbSelectBlock']     = '#f0f0f8'
  va['rgbSearchBg']        = va['rgbDarkBg']
  va['rgbBreadcumb']       = '#e0e0fc'
  va['rgbBreadcumbBg']     = va['rgbLightBg']
  va['rgbANavTopLink']     = '#fff'
  va['rgbAHoverTopBg']     = va['rgbLightBg']
  va['rgbAHoverBg']        = va['rgbDarkBg']
  va['rgbANavTopLink']     = '#fff'
  va['rgbAHoverTopBg']     = va['rgbLightBg']
  va['rgbTabHeaderBg']     = va['rgbLightBg']
  va['rgbTabHeaderText']   = '#080683'
  va['rgbFrameBorder']     = va['rgbDarkBg']
  va['rgbFrameHeaderBg']   = va['rgbLightBg']
  save_css ( name, va )

  #name = 'hkm'
  #va = v
  #va['rgbDarkBg']          = '#3a5298'
  #va['rgbLightBg']         = '#9eb6fc'
  #va['rgbTabHeaderBgExt'] = va['rgbDarkBg']
  #va['rgbSelectBlock']     = '#f0f0f8'
  #va['rgbSearchBg']        = va['rgbDarkBg']
  #va['rgbBreadcumb']       = '#e0e0fc'
  #va['rgbBreadcumbBg']     = va['rgbLightBg']
  #va['rgbANavTopLink']     = '#fff'
  #va['rgbAHoverTopBg']     = va['rgbLightBg']
  #va['rgbAHoverBg']        = va['rgbDarkBg']
  #va['rgbANavTopLink']     = '#fff'
  #va['rgbAHoverTopBg']     = va['rgbLightBg']
  #va['rgbTabHeaderBg']     = va['rgbLightBg']
  #va['rgbTabHeaderText']   = '#080683'
  #va['rgbFrameBorder']     = va['rgbDarkBg']
  #va['rgbFrameHeaderBg']   = va['rgbLightBg']
  #save_css ( name, va )

  name = 'portfolio'
  va = copy.copy ( v )
  va['rgbDarkBg']          = '#3492b2'
  va['rgbLightBg']         = '#bad8e3'
  va['rgbTabHeaderBgExt']  = va['rgbDarkBg']
  va['rgbFrameBg']         = '#f4f4f8'
  va['rgbSelectBlock']     = '#f0f0f8'
  va['rgbSearchBg']        = va['rgbDarkBg']
  va['rgbBreadcumb']       = '#e0e0fc'
  va['rgbBreadcumbBg']     = va['rgbLightBg']
  va['rgbANavTopLink']     = '#fff'
  va['rgbAHoverTopBg']     = va['rgbLightBg']
  va['rgbAHoverBg']        = va['rgbDarkBg']
  va['rgbANavTopLink']     = '#fff'
  va['rgbAHoverTopBg']     = va['rgbLightBg']
  va['rgbTabHeaderBg']     = va['rgbLightBg']
  va['rgbTabHeaderText']   = '#080683'
  va['rgbFrameBorder']     = va['rgbDarkBg']
  va['rgbFrameHeaderBg']   = va['rgbLightBg']
  va['rgbANavHeadLink']    = '#fff'
  va['rgbHead2']           = '#fff'
  va['rgbSearchBg']        = '#fff'
  va['rgbBreadcumbBg']     = '#7fa5b9'
  save_css ( name, va )

  name = 'ssa'
  va = copy.copy ( v )
  va['rgbDarkBg']          = '#7c931b'
  va['rgbLightBg']         = '#ccde83'
  va['rgbTabHeaderBgExt']  = va['rgbDarkBg']
  va['rgbFrameBg']         = '#f4f4d8'
  va['rgbSelectBlock']     = '#f0f0c8'
  va['rgbIntroBlock']      = '#d8eb8a'
  va['rgbSearchBg']        = va['rgbDarkBg']
  va['rgbBreadcumb']       = '#e0e0fc'
  va['rgbBreadcumbBg']     = va['rgbLightBg']
  va['rgbANavTopLink']     = '#fff'
  va['rgbAHoverTopBg']     = va['rgbLightBg']
  va['rgbAHoverBg']        = va['rgbDarkBg']
  va['rgbANavTopLink']     = '#fff'
  va['rgbAHoverTopBg']     = va['rgbLightBg']
  va['rgbTabHeaderBg']     = va['rgbLightBg']
  va['rgbTabHeaderText']   = '#080683'
  va['rgbFrameBorder']     = va['rgbDarkBg']
  va['rgbFrameHeaderBg']   = va['rgbLightBg']
  va['rgbInput']           = '#7c931b'
  save_css ( name, va )

  name = 'tour'
  va = copy.copy ( v )
  va['nWidth']             = 50
  va['nWidth_05']          = -50 + 5
  va['nWidth_10']          = 50 - 10
  va['nMarginLeft']        = 20
  va['nMarginRight']       = 0
  va['rgbIndexTab']        = '#606068'
  va['rgbTabHeaderBg']     = '#e8e8f0'
  va['rgbHeaderBlock']     = '#a096cc'
  va['rgbBorderTopLeft']   = '#b0b0b8'
  va['rgbBorderBottomRight'] = '#606068'
  va['rgbFooterColor']       = va['rgbBorderBottomRight']
  save_css ( name, va )

  name = 'webquest'
  va = copy.copy ( v )
  va['rgbDarkBg']          = '#3492b2'
  va['rgbLightBg']         = '#bad8e3'
  va['rgbTabHeaderBgExt']  = va['rgbDarkBg']
  va['rgbFrameBg']         = '#f4f4f8'
  va['rgbSelectBlock']     = '#f0f0f8'
  va['rgbSearchBg']        = va['rgbDarkBg']
  va['rgbBreadcumb']       = '#e0e0fc'
  va['rgbBreadcumbBg']     = va['rgbLightBg']
  va['rgbANavTopLink']     = '#fff'
  va['rgbAHoverTopBg']     = va['rgbLightBg']
  va['rgbAHoverBg']        = va['rgbDarkBg']
  va['rgbANavTopLink']     = '#fff'
  va['rgbAHoverTopBg']     = va['rgbLightBg']
  va['rgbTabHeaderBg']     = va['rgbLightBg']
  va['rgbTabHeaderText']   = '#080683'
  va['rgbFrameBorder']     = va['rgbDarkBg']
  va['rgbFrameHeaderBg']   = va['rgbLightBg']
  va['rgbANavHeadLink']    = '#fff'
  va['rgbHead2']           = '#fff'
  va['rgbSearchBg']        = '#fff'
  va['rgbBreadcumbBg']     = '#7fa5b9'
  save_css ( name, va )

  item_container = get_top_item_container()
  app_name = 'css_generator'
  vars = get_item_vars_show(request, item_container, app_name)
  vars['title'] = _(u'Erzeugen der CSS-Stylesheet-Dateien')
  return render_to_response ( 'base-full-width.html', vars )
