#!/usr/bin/python
#-*-coding: utf-8 -*-
"""
Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.

0.01  31.01.2008  Userfolder fuer Newsletter der Grundschulen belegen
"""

from django.utils.encoding  import smart_unicode

from dms.models   import DmsUserUrlRole
from dms.queries  import get_users_with_email_by_org_id
from dms.queries  import get_containers_by_path
from dms.queries  import get_role_by_name

from dms.settings import *
from dms.encode_decode import decode_html

# Die folgenden Schulnummern muessen zukuenftig direkt aus den Daten der Schulen gewonnen werden

d_grundschulen = {8201: 1, 8202: 1, 8203: 1, 8204: 1, 8205: 1, 8206: 1, 8207: 1, 8208: 1, 8209: 1, 8210: 1, 8211: 1, 8212: 1, 8213: 1, 8214: 1, 8216: 1, 8217: 1, 8219: 1, 8220: 1, 8221: 1, 8222: 1, 8223: 1, 8224: 1, 8225: 1, 8226: 1, 8230: 1, 8232: 1, 8233: 1, 8234: 1, 8236: 1, 8237: 1, 8238: 1, 8239: 1, 8240: 1, 8242: 1, 8244: 1, 8245: 1, 8246: 1, 8247: 1, 8248: 1, 8249: 1, 8250: 1, 8251: 1, 8252: 1, 8255: 1, 8256: 1, 8257: 1, 8258: 1, 8261: 1, 8262: 1, 8263: 1, 8264: 1, 8265: 1, 8266: 1, 8267: 1, 8268: 1, 8270: 1, 8271: 1, 8272: 1, 8273: 1, 8274: 1, 8275: 1, 8276: 1, 8277: 1, 8278: 1, 8279: 1, 8280: 1, 3100: 1, 3101: 1, 3102: 1, 3103: 1, 3104: 1, 3105: 1, 3106: 1, 3107: 1, 3109: 1, 3111: 1, 3112: 1, 3113: 1, 3114: 1, 3115: 1, 3116: 1, 3117: 1, 3118: 1, 3120: 1, 3121: 1, 3122: 1, 3123: 1, 3124: 1, 3125: 1, 3127: 1, 3128: 1, 3129: 1, 3130: 1, 3131: 1, 3132: 1, 3133: 1, 3134: 1, 3135: 1, 3136: 1, 3137: 1, 3138: 1, 3148: 1, 3149: 1, 3150: 1, 3151: 1, 3152: 1, 3153: 1, 3154: 1, 3155: 1, 3156: 1, 3158: 1, 3159: 1, 3160: 1, 3161: 1, 3162: 1, 3163: 1, 3164: 1, 3165: 1, 3166: 1, 3167: 1, 3168: 1, 3169: 1, 3170: 1, 3171: 1, 3172: 1, 3173: 1, 3174: 1, 3176: 1, 3177: 1, 3178: 1, 3179: 1, 3184: 1, 3185: 1, 3186: 1, 3187: 1, 3188: 1, 3189: 1, 3190: 1, 3191: 1, 3193: 1, 3194: 1, 3195: 1, 3196: 1, 3197: 1, 3198: 1, 3201: 1, 3202: 1, 3204: 1, 3205: 1, 3208: 1, 3209: 1, 3211: 1, 3212: 1, 3213: 1, 3215: 1, 3216: 1, 3217: 1, 3219: 1, 3221: 1, 3223: 1, 3224: 1, 3227: 1, 3228: 1, 3229: 1, 3230: 1, 3231: 1, 3232: 1, 3233: 1, 3235: 1, 3236: 1, 3237: 1, 3239: 1, 3240: 1, 3241: 1, 3242: 1, 3243: 1, 3245: 1, 3246: 1, 3247: 1, 3248: 1, 3250: 1, 3251: 1, 3253: 1, 3255: 1, 3256: 1, 3257: 1, 3259: 1, 3262: 1, 3263: 1, 3264: 1, 3265: 1, 3266: 1, 3268: 1, 3269: 1, 3270: 1, 3271: 1, 3272: 1, 3274: 1, 3275: 1, 3276: 1, 3277: 1, 3280: 1, 3281: 1, 3282: 1, 3283: 1, 3285: 1, 3286: 1, 3288: 1, 3290: 1, 3291: 1, 3292: 1, 3293: 1, 3294: 1, 3296: 1, 3298: 1, 3300: 1, 3301: 1, 3304: 1, 3305: 1, 3306: 1, 3309: 1, 3311: 1, 3312: 1, 3313: 1, 3316: 1, 3318: 1, 3321: 1, 3322: 1, 3323: 1, 3324: 1, 3325: 1, 3331: 1, 3332: 1, 3333: 1, 3334: 1, 3338: 1, 3341: 1, 3344: 1, 3345: 1, 3347: 1, 3348: 1, 3349: 1, 3350: 1, 3351: 1, 3352: 1, 3354: 1, 3355: 1, 3357: 1, 3358: 1, 3362: 1, 3363: 1, 3364: 1, 3366: 1, 3369: 1, 3370: 1, 3371: 1, 3374: 1, 3375: 1, 3378: 1, 3379: 1, 3380: 1, 3384: 1, 3385: 1, 3386: 1, 3388: 1, 3389: 1, 3390: 1, 3391: 1, 3393: 1, 3394: 1, 3397: 1, 3398: 1, 3399: 1, 3400: 1, 3401: 1, 3403: 1, 3405: 1, 3407: 1, 3408: 1, 3409: 1, 3411: 1, 3413: 1, 3414: 1, 3415: 1, 3416: 1, 3418: 1, 3419: 1, 3420: 1, 3425: 1, 3426: 1, 3429: 1, 3430: 1, 3431: 1, 3432: 1, 3433: 1, 3435: 1, 3436: 1, 3437: 1, 3438: 1, 3439: 1, 3440: 1, 3444: 1, 3448: 1, 3451: 1, 3452: 1, 3453: 1, 3454: 1, 3457: 1, 3464: 1, 3479: 1, 3480: 1, 3481: 1, 3482: 1, 3483: 1, 3485: 1, 3486: 1, 3488: 1, 3489: 1, 3491: 1, 3492: 1, 3500: 1, 3501: 1, 3502: 1, 3503: 1, 3506: 1, 3507: 1, 3509: 1, 3510: 1, 3511: 1, 3512: 1, 3514: 1, 3516: 1, 3518: 1, 3519: 1, 3521: 1, 3522: 1, 3523: 1, 3525: 1, 3528: 1, 3529: 1, 3530: 1, 3531: 1, 3532: 1, 3533: 1, 3534: 1, 3536: 1, 3537: 1, 3538: 1, 3539: 1, 3540: 1, 3542: 1, 3543: 1, 3544: 1, 3545: 1, 3546: 1, 3548: 1, 3549: 1, 3550: 1, 3551: 1, 3552: 1, 3553: 1, 3555: 1, 3556: 1, 3558: 1, 3559: 1, 3560: 1, 3561: 1, 3562: 1, 3563: 1, 3565: 1, 3566: 1, 3567: 1, 3571: 1, 3572: 1, 3573: 1, 3578: 1, 3579: 1, 3580: 1, 3582: 1, 3583: 1, 3585: 1, 3587: 1, 3588: 1, 3590: 1, 3591: 1, 3592: 1, 3593: 1, 3594: 1, 3599: 1, 3602: 1, 3603: 1, 3604: 1, 3605: 1, 3606: 1, 3608: 1, 3609: 1, 3612: 1, 3614: 1, 3617: 1, 3618: 1, 3619: 1, 3622: 1, 3623: 1, 3624: 1, 3627: 1, 3628: 1, 3629: 1, 3630: 1, 3631: 1, 3633: 1, 3635: 1, 3636: 1, 3638: 1, 3639: 1, 3642: 1, 3643: 1, 3644: 1, 3646: 1, 3648: 1, 3650: 1, 3651: 1, 3653: 1, 3654: 1, 3656: 1, 3659: 1, 3660: 1, 3661: 1, 3662: 1, 3665: 1, 3666: 1, 3667: 1, 3669: 1, 3670: 1, 3671: 1, 3672: 1, 3674: 1, 3676: 1, 3677: 1, 3678: 1, 3679: 1, 3680: 1, 3681: 1, 3683: 1, 3687: 1, 3688: 1, 3689: 1, 3690: 1, 3694: 1, 3695: 1, 3696: 1, 3697: 1, 3698: 1, 3699: 1, 3700: 1, 3701: 1, 3702: 1, 3703: 1, 3704: 1, 3705: 1, 3706: 1, 3708: 1, 3710: 1, 3711: 1, 3712: 1, 3714: 1, 3716: 1, 3722: 1, 3724: 1, 3725: 1, 3726: 1, 3727: 1, 3729: 1, 3730: 1, 3731: 1, 3733: 1, 3735: 1, 3740: 1, 3741: 1, 3742: 1, 3743: 1, 3744: 1, 3745: 1, 3753: 1, 3755: 1, 3758: 1, 3759: 1, 3761: 1, 3763: 1, 3764: 1, 3766: 1, 3767: 1, 3768: 1, 3769: 1, 3770: 1, 3772: 1, 3773: 1, 3774: 1, 3775: 1, 3776: 1, 3778: 1, 3779: 1, 3780: 1, 3781: 1, 3782: 1, 3784: 1, 3785: 1, 3787: 1, 3789: 1, 3791: 1, 3792: 1, 3793: 1, 3794: 1, 3795: 1, 3796: 1, 3797: 1, 3798: 1, 3799: 1, 3801: 1, 3803: 1, 3807: 1, 3808: 1, 3809: 1, 3810: 1, 3811: 1, 3812: 1, 3813: 1, 3814: 1, 3815: 1, 3817: 1, 3818: 1, 3819: 1, 3820: 1, 3821: 1, 3822: 1, 3824: 1, 3825: 1, 3826: 1, 3827: 1, 3828: 1, 3829: 1, 3830: 1, 3831: 1, 3832: 1, 3833: 1, 3834: 1, 3835: 1, 3837: 1, 3838: 1, 3839: 1, 3840: 1, 3841: 1, 3842: 1, 3843: 1, 3844: 1, 3845: 1, 3846: 1, 3847: 1, 3848: 1, 3849: 1, 3850: 1, 3851: 1, 3852: 1, 3853: 1, 3858: 1, 3861: 1, 3862: 1, 3869: 1, 3873: 1, 3875: 1, 3876: 1, 3877: 1, 3878: 1, 3879: 1, 3880: 1, 3881: 1, 3882: 1, 3883: 1, 3884: 1, 3885: 1, 3886: 1, 3887: 1, 3888: 1, 3889: 1, 3890: 1, 3891: 1, 3892: 1, 3893: 1, 3894: 1, 3895: 1, 3897: 1, 3899: 1, 3900: 1, 3902: 1, 3903: 1, 3904: 1, 3905: 1, 3906: 1, 3907: 1, 3908: 1, 3909: 1, 3910: 1, 3911: 1, 3912: 1, 3913: 1, 3914: 1, 3915: 1, 3917: 1, 3918: 1, 3919: 1, 3920: 1, 3921: 1, 3922: 1, 3923: 1, 3925: 1, 3926: 1, 3927: 1, 3928: 1, 3929: 1, 3930: 1, 3931: 1, 3932: 1, 3933: 1, 3934: 1, 3935: 1, 3936: 1, 3937: 1, 3939: 1, 3940: 1, 3941: 1, 3942: 1, 3943: 1, 3945: 1, 3946: 1, 3948: 1, 3949: 1, 3950: 1, 3952: 1, 3954: 1, 3955: 1, 3956: 1, 3958: 1, 3959: 1, 3960: 1, 3961: 1, 3965: 1, 3967: 1, 3972: 1, 3974: 1, 3975: 1, 3976: 1, 3979: 1, 3980: 1, 3982: 1, 3990: 1, 3993: 1, 3994: 1, 3996: 1, 3997: 1, 3998: 1, 3999: 1, 4000: 1, 4001: 1, 4002: 1, 4003: 1, 4004: 1, 4005: 1, 4006: 1, 4007: 1, 4008: 1, 4009: 1, 4010: 1, 4011: 1, 4012: 1, 4013: 1, 4014: 1, 4015: 1, 4016: 1, 4017: 1, 4018: 1, 4020: 1, 4022: 1, 4023: 1, 4024: 1, 4026: 1, 4027: 1, 4029: 1, 4030: 1, 4031: 1, 4032: 1, 4033: 1, 4036: 1, 4037: 1, 4040: 1, 4041: 1, 4042: 1, 4045: 1, 4046: 1, 4047: 1, 4048: 1, 4049: 1, 4050: 1, 4052: 1, 4053: 1, 4054: 1, 4055: 1, 4056: 1, 4059: 1, 4060: 1, 4061: 1, 4062: 1, 4063: 1, 4065: 1, 4066: 1, 4068: 1, 4069: 1, 4070: 1, 4072: 1, 4074: 1, 4075: 1, 4076: 1, 4077: 1, 4078: 1, 4079: 1, 4081: 1, 4082: 1, 4083: 1, 4086: 1, 4088: 1, 4090: 1, 4091: 1, 4093: 1, 4095: 1, 4096: 1, 4097: 1, 4098: 1, 4099: 1, 4100: 1, 4101: 1, 4103: 1, 4104: 1, 4108: 1, 4109: 1, 4110: 1, 4111: 1, 4114: 1, 4116: 1, 4117: 1, 4119: 1, 4122: 1, 4124: 1, 4125: 1, 4127: 1, 4128: 1, 4129: 1, 4130: 1, 4132: 1, 4133: 1, 4135: 1, 4137: 1, 4139: 1, 4140: 1, 4141: 1, 4142: 1, 4143: 1, 4144: 1, 4145: 1, 4146: 1, 4147: 1, 4148: 1, 4149: 1, 4150: 1, 4151: 1, 4152: 1, 4153: 1, 4154: 1, 4155: 1, 4156: 1, 4157: 1, 4158: 1, 4159: 1, 4160: 1, 4161: 1, 4162: 1, 4163: 1, 4164: 1, 4165: 1, 4166: 1, 4168: 1, 4169: 1, 4170: 1, 4171: 1, 4172: 1, 4173: 1, 4175: 1, 4176: 1, 4177: 1, 4178: 1, 4179: 1, 4180: 1, 4181: 1, 4182: 1, 4183: 1, 4186: 1, 4188: 1, 4189: 1, 4190: 1, 4191: 1, 4192: 1, 4193: 1, 4194: 1, 4196: 1, 4199: 1, 4201: 1, 4202: 1, 4203: 1, 4204: 1, 4208: 1, 4209: 1, 4211: 1, 4212: 1, 4213: 1, 4214: 1, 4220: 1, 4221: 1, 4222: 1, 4224: 1, 4225: 1, 4226: 1, 4229: 1, 4230: 1, 4231: 1, 4232: 1, 4233: 1, 4234: 1, 4235: 1, 4236: 1, 4237: 1, 4238: 1, 4239: 1, 4243: 1, 4246: 1, 4248: 1, 4249: 1, 4250: 1, 4251: 1, 4252: 1, 4253: 1, 4254: 1, 4256: 1, 4257: 1, 4261: 1, 4262: 1, 4264: 1, 4266: 1, 4268: 1, 4271: 1, 4272: 1, 4273: 1, 4277: 1, 4278: 1, 4279: 1, 4280: 1, 4281: 1, 4282: 1, 4283: 1, 4284: 1, 4285: 1, 4287: 1, 4288: 1, 4289: 1, 4290: 1, 4292: 1, 4293: 1, 4295: 1, 4297: 1, 4298: 1, 4299: 1, 4300: 1, 4301: 1, 4302: 1, 4303: 1, 4304: 1, 4305: 1, 4306: 1, 4307: 1, 4308: 1, 4309: 1, 4310: 1, 4311: 1, 4312: 1, 4313: 1, 4314: 1, 4316: 1, 4317: 1, 4319: 1, 4320: 1, 4321: 1, 4324: 1, 4325: 1, 4326: 1, 4327: 1, 4328: 1, 4330: 1, 4380: 1, 4381: 1, 4430: 1, 4530: 1, 4601: 1, 4602: 1, 4604: 1, 4605: 1, 4606: 1, 4607: 1, 4608: 1, 4609: 1, 4610: 1, 4611: 1, 4612: 1, 4614: 1, 4615: 1, 4616: 1, 4619: 1, 4622: 1, 4623: 1, 4624: 1, 4626: 1, 4627: 1, 4628: 1, 4629: 1, 4630: 1, 4631: 1, 4632: 1, 4633: 1, 4634: 1, 4635: 1, 4636: 1, 4637: 1, 4638: 1, 4639: 1, 4640: 1, 4642: 1, 4643: 1, 4645: 1, 4647: 1, 4649: 1, 4650: 1, 4652: 1, 4654: 1, 4655: 1, 4656: 1, 4657: 1, 4659: 1, 4660: 1, 4661: 1, 4662: 1, 4663: 1, 4664: 1, 4666: 1, 4668: 1, 4669: 1, 4671: 1, 4672: 1, 4673: 1, 4674: 1, 4675: 1, 4677: 1, 4679: 1, 4681: 1, 4683: 1, 4684: 1, 4685: 1, 4686: 1, 4688: 1, 4691: 1, 4692: 1, 4693: 1, 4694: 1, 4695: 1, 4696: 1, 4697: 1, 4698: 1, 4700: 1, 4702: 1, 4703: 1, 4704: 1, 4705: 1, 4706: 1, 4707: 1, 4709: 1, 4711: 1, 4712: 1, 4713: 1, 4714: 1, 4715: 1, 4716: 1, 4717: 1, 4718: 1, 4719: 1, 4720: 1, 4721: 1, 4722: 1, 4723: 1, 4724: 1, 4725: 1, 4726: 1, 4727: 1, 4728: 1, 4729: 1, 4730: 1, 4731: 1, 4732: 1, 4733: 1, 4734: 1, 4735: 1, 4736: 1, 4739: 1, 4740: 1, 4741: 1, 4742: 1, 4743: 1, 4745: 1, 4747: 1, 4749: 1, 4750: 1, 4751: 1, 4752: 1, 4753: 1, 4754: 1, 4755: 1, 4756: 1, 4757: 1, 4758: 1, 4759: 1, 4760: 1, 4761: 1, 4762: 1, 4763: 1, 4764: 1, 4765: 1, 4767: 1, 4768: 1, 4770: 1, 4771: 1, 4773: 1, 4774: 1, 4775: 1, 4776: 1, 4777: 1, 4778: 1, 4779: 1, 4780: 1, 4781: 1, 4782: 1, 4783: 1, 4784: 1, 4785: 1, 4786: 1, 4787: 1, 4788: 1, 4789: 1, 4790: 1, 4791: 1, 4861: 1, 4930: 1, 5024: 1, 5238: 1, 7100: 1, 7102: 1, 7103: 1, 7104: 1, 7105: 1, 7106: 1, 7107: 1, 7108: 1, 7109: 1, 7110: 1, 7111: 1, 7112: 1, 7113: 1, 7114: 1, 7115: 1, 7116: 1, 7119: 1, 7120: 1, 7121: 1, 7123: 1, 7124: 1, 7125: 1, 7127: 1, 7129: 1, 7130: 1, 7131: 1, 7132: 1, 7133: 1, 7134: 1, 7135: 1, 7136: 1, 7137: 1, 7138: 1, 7139: 1, 7141: 1, 7142: 1, 7143: 1, 7144: 1, 7145: 1, 7146: 1, 7148: 1, 7150: 1, 7151: 1, 7154: 1, 7156: 1, 7157: 1, 7158: 1, 7159: 1, 7161: 1, 7162: 1, 7165: 1, 7170: 1, 7173: 1, 7174: 1, 7178: 1, 7180: 1, 7182: 1, 7184: 1, 7185: 1, 7186: 1, 7189: 1, 7190: 1, 7191: 1, 7192: 1, 7194: 1, 7196: 1, 7197: 1, 7199: 1, 7202: 1, 7204: 1, 7205: 1, 7207: 1, 7212: 1, 7214: 1, 7215: 1, 7216: 1, 7218: 1, 7219: 1, 7220: 1, 7221: 1, 7223: 1, 7227: 1, 7229: 1, 7230: 1, 7231: 1, 7232: 1, 7233: 1, 7234: 1, 7235: 1, 7236: 1, 7237: 1, 7238: 1, 7239: 1, 7240: 1, 7244: 1, 7245: 1, 7248: 1, 7249: 1, 7252: 1, 7254: 1, 7255: 1, 7256: 1, 7258: 1, 7260: 1, 7261: 1, 7263: 1, 7265: 1, 7266: 1, 7267: 1, 7271: 1, 7272: 1, 7273: 1, 7276: 1, 7279: 1, 7281: 1, 7283: 1, 7285: 1, 7286: 1, 7287: 1, 7288: 1, 7289: 1, 7290: 1, 7291: 1, 7292: 1, 7293: 1, 7294: 1, 7295: 1, 7299: 1, 7300: 1, 7302: 1, 7305: 1, 7306: 1, 7307: 1, 7308: 1, 7309: 1, 7311: 1, 7312: 1, 7313: 1, 7315: 1, 7316: 1, 7318: 1, 7322: 1, 7330: 1, 7331: 1, 7334: 1, 7337: 1, 7338: 1, 7340: 1, 7341: 1, 7342: 1, 7344: 1, 7345: 1, 7346: 1, 7347: 1, 7348: 1, 7350: 1, 7351: 1, 7354: 1, 7355: 1, 7356: 1, 7357: 1, 7358: 1, 7362: 1, 7367: 1, 7371: 1, 7372: 1, 7373: 1, 7376: 1, 7379: 1, 7380: 1, 7382: 1, 7385: 1, 7387: 1, 7388: 1, 7390: 1, 7392: 1, 7393: 1, 7394: 1, 7395: 1, 7396: 1, 7397: 1, 7398: 1, 7399: 1, 7400: 1, 7401: 1, 7402: 1, 7403: 1, 7404: 1, 7405: 1, 7406: 1, 7407: 1, 7408: 1, 7409: 1, 7411: 1, 7413: 1, 7416: 1, 7417: 1, 7418: 1, 7419: 1, 7420: 1, 7421: 1, 7422: 1, 7424: 1, 7426: 1, 7427: 1, 7428: 1, 7430: 1, 7433: 1, 7435: 1, 7437: 1, 7439: 1, 7440: 1, 7441: 1, 7442: 1, 7443: 1, 7446: 1, 7448: 1, 7452: 1, 7455: 1, 7456: 1, 7457: 1, 7458: 1, 7459: 1, 7460: 1, 7462: 1, 7464: 1, 7465: 1, 7466: 1, 7469: 1, 7470: 1, 7471: 1, 7472: 1, 7473: 1, 7475: 1, 7479: 1, 7482: 1, 7485: 1, 7486: 1, 7488: 1, 7489: 1, 7490: 1, 7491: 1, 7503: 1, 7505: 1, 7507: 1, 7508: 1, 7510: 1, 7512: 1, 7516: 1, 7517: 1, 7519: 1, 7522: 1, 7524: 1, 7526: 1, 7528: 1, 7530: 1, 7537: 1, 7540: 1, 7542: 1, 7544: 1, 7545: 1, 7549: 1, 7554: 1, 7555: 1, 7556: 1, 7559: 1, 7560: 1, 7561: 1, 7566: 1, 7567: 1, 7568: 1, 7569: 1, 7571: 1, 7572: 1, 7573: 1, 7574: 1, 7575: 1, 7577: 1, 7578: 1, 7579: 1, 7580: 1, 7581: 1, 7582: 1, 7583: 1, 7584: 1, 7586: 1, 7588: 1, 7589: 1, 7591: 1, 7593: 1, 7598: 1, 7600: 1, 7602: 1, 7604: 1, 7605: 1, 7607: 1, 7609: 1, 7612: 1, 7616: 1, 7617: 1, 7621: 1, 7627: 1, 7629: 1, 7630: 1, 7631: 1, 7632: 1, 7634: 1, 7636: 1, 7637: 1, 7640: 1, 7642: 1, 7643: 1, 7645: 1, 7646: 1, 7647: 1, 7648: 1, 7649: 1, 7650: 1, 7651: 1, 7652: 1, 7653: 1, 7655: 1, 7656: 1, 7657: 1, 7658: 1, 7660: 1, 7661: 1, 7662: 1, 7663: 1, 7664: 1, 7665: 1, 7668: 1, 7669: 1, 7670: 1, 7671: 1, 7672: 1, 7673: 1, 7674: 1, 7677: 1, 7678: 1, 7679: 1, 7680: 1, 7681: 1, 7682: 1, 7683: 1, 7684: 1}

l_grundschulen = [3100, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3109, 3111, 3112, 3113, 3114, 3115, 3116, 3117, 3118, 3120, 3121, 3122, 3123, 3124, 3125, 3127, 3128, 3129, 3130, 3131, 3132, 3133, 3134, 3135, 3136, 3137, 3138, 3148, 3149, 3150, 3151, 3152, 3153, 3154, 3155, 3156, 3158, 3159, 3160, 3161, 3162, 3163, 3164, 3165, 3166, 3167, 3168, 3169, 3170, 3171, 3172, 3173, 3174, 3176, 3177, 3178, 3179, 3184, 3185, 3186, 3187, 3188, 3189, 3190, 3191, 3193, 3194, 3195, 3196, 3197, 3198, 3201, 3202, 3204, 3205, 3208, 3209, 3211, 3212, 3213, 3215, 3216, 3217, 3219, 3221, 3223, 3224, 3227, 3228, 3229, 3230, 3231, 3232, 3233, 3235, 3236, 3237, 3239, 3240, 3241, 3242, 3243, 3245, 3246, 3247, 3248, 3250, 3251, 3253, 3255, 3256, 3257, 3259, 3262, 3263, 3264, 3265, 3266, 3268, 3269, 3270, 3271, 3272, 3274, 3275, 3276, 3277, 3280, 3281, 3282, 3283, 3285, 3286, 3288, 3290, 3291, 3292, 3293, 3294, 3296, 3298, 3300, 3301, 3304, 3305, 3306, 3309, 3311, 3312, 3313, 3316, 3318, 3321, 3322, 3323, 3324, 3325, 3331, 3332, 3333, 3334, 3338, 3341, 3344, 3345, 3347, 3348, 3349, 3350, 3351, 3352, 3354, 3355, 3357, 3358, 3362, 3363, 3364, 3366, 3369, 3370, 3371, 3374, 3375, 3378, 3379, 3380, 3384, 3385, 3386, 3388, 3389, 3390, 3391, 3393, 3394, 3397, 3398, 3399, 3400, 3401, 3403, 3405, 3407, 3408, 3409, 3411, 3413, 3414, 3415, 3416, 3418, 3419, 3420, 3425, 3426, 3429, 3430, 3431, 3432, 3433, 3435, 3436, 3437, 3438, 3439, 3440, 3444, 3448, 3451, 3452, 3453, 3454, 3457, 3464, 3479, 3480, 3481, 3482, 3483, 3485, 3486, 3488, 3489, 3491, 3492, 3500, 3501, 3502, 3503, 3506, 3507, 3509, 3510, 3511, 3512, 3514, 3516, 3518, 3519, 3521, 3522, 3523, 3525, 3528, 3529, 3530, 3531, 3532, 3533, 3534, 3536, 3537, 3538, 3539, 3540, 3542, 3543, 3544, 3545, 3546, 3548, 3549, 3550, 3551, 3552, 3553, 3555, 3556, 3558, 3559, 3560, 3561, 3562, 3563, 3565, 3566, 3567, 3571, 3572, 3573, 3578, 3579, 3580, 3582, 3583, 3585, 3587, 3588, 3590, 3591, 3592, 3593, 3594, 3599, 3602, 3603, 3604, 3605, 3606, 3608, 3609, 3612, 3614, 3617, 3618, 3619, 3622, 3623, 3624, 3627, 3628, 3629, 3630, 3631, 3633, 3635, 3636, 3638, 3639, 3642, 3643, 3644, 3646, 3648, 3650, 3651, 3653, 3654, 3656, 3659, 3660, 3661, 3662, 3665, 3666, 3667, 3669, 3670, 3671, 3672, 3674, 3676, 3677, 3678, 3679, 3680, 3681, 3683, 3687, 3688, 3689, 3690, 3694, 3695, 3696, 3697, 3698, 3699, 3700, 3701, 3702, 3703, 3704, 3705, 3706, 3708, 3710, 3711, 3712, 3714, 3716, 3722, 3724, 3725, 3726, 3727, 3729, 3730, 3731, 3733, 3735, 3740, 3741, 3742, 3743, 3744, 3745, 3753, 3755, 3758, 3759, 3761, 3763, 3764, 3766, 3767, 3768, 3769, 3770, 3772, 3773, 3774, 3775, 3776, 3778, 3779, 3780, 3781, 3782, 3784, 3785, 3787, 3789, 3791, 3792, 3793, 3794, 3795, 3796, 3797, 3798, 3799, 3801, 3803, 3807, 3808, 3809, 3810, 3811, 3812, 3813, 3814, 3815, 3817, 3818, 3819, 3820, 3821, 3822, 3824, 3825, 3826, 3827, 3828, 3829, 3830, 3831, 3832, 3833, 3834, 3835, 3837, 3838, 3839, 3840, 3841, 3842, 3843, 3844, 3845, 3846, 3847, 3848, 3849, 3850, 3851, 3852, 3853, 3858, 3861, 3862, 3869, 3873, 3875, 3876, 3877, 3878, 3879, 3880, 3881, 3882, 3883, 3884, 3885, 3886, 3887, 3888, 3889, 3890, 3891, 3892, 3893, 3894, 3895, 3897, 3899, 3900, 3902, 3903, 3904, 3905, 3906, 3907, 3908, 3909, 3910, 3911, 3912, 3913, 3914, 3915, 3917, 3918, 3919, 3920, 3921, 3922, 3923, 3925, 3926, 3927, 3928, 3929, 3930, 3931, 3932, 3933, 3934, 3935, 3936, 3937, 3939, 3940, 3941, 3942, 3943, 3945, 3946, 3948, 3949, 3950, 3952, 3954, 3955, 3956, 3958, 3959, 3960, 3961, 3965, 3967, 3972, 3974, 3975, 3976, 3979, 3980, 3982, 3990, 3993, 3994, 3996, 3997, 3998, 3999, 4000, 4001, 4002, 4003, 4004, 4005, 4006, 4007, 4008, 4009, 4010, 4011, 4012, 4013, 4014, 4015, 4016, 4017, 4018, 4020, 4022, 4023, 4024, 4026, 4027, 4029, 4030, 4031, 4032, 4033, 4036, 4037, 4040, 4041, 4042, 4045, 4046, 4047, 4048, 4049, 4050, 4052, 4053, 4054, 4055, 4056, 4059, 4060, 4061, 4062, 4063, 4065, 4066, 4068, 4069, 4070, 4072, 4074, 4075, 4076, 4077, 4078, 4079, 4081, 4082, 4083, 4086, 4088, 4090, 4091, 4093, 4095, 4096, 4097, 4098, 4099, 4100, 4101, 4103, 4104, 4108, 4109, 4110, 4111, 4114, 4116, 4117, 4119, 4122, 4124, 4125, 4127, 4128, 4129, 4130, 4132, 4133, 4135, 4137, 4139, 4140, 4141, 4142, 4143, 4144, 4145, 4146, 4147, 4148, 4149, 4150, 4151, 4152, 4153, 4154, 4155, 4156, 4157, 4158, 4159, 4160, 4161, 4162, 4163, 4164, 4165, 4166, 4168, 4169, 4170, 4171, 4172, 4173, 4175, 4176, 4177, 4178, 4179, 4180, 4181, 4182, 4183, 4186, 4188, 4189, 4190, 4191, 4192, 4193, 4194, 4196, 4199, 4201, 4202, 4203, 4204, 4208, 4209, 4211, 4212, 4213, 4214, 4220, 4221, 4222, 4224, 4225, 4226, 4229, 4230, 4231, 4232, 4233, 4234, 4235, 4236, 4237, 4238, 4239, 4243, 4246, 4248, 4249, 4250, 4251, 4252, 4253, 4254, 4256, 4257, 4261, 4262, 4264, 4266, 4268, 4271, 4272, 4273, 4277, 4278, 4279, 4280, 4281, 4282, 4283, 4284, 4285, 4287, 4288, 4289, 4290, 4292, 4293, 4295, 4297, 4298, 4299, 4300, 4301, 4302, 4303, 4304, 4305, 4306, 4307, 4308, 4309, 4310, 4311, 4312, 4313, 4314, 4316, 4317, 4319, 4320, 4321, 4324, 4325, 4326, 4327, 4328, 4330, 4380, 4381, 4430, 4530, 4601, 4602, 4604, 4605, 4606, 4607, 4608, 4609, 4610, 4611, 4612, 4614, 4615, 4616, 4619, 4622, 4623, 4624, 4626, 4627, 4628, 4629, 4630, 4631, 4632, 4633, 4634, 4635, 4636, 4637, 4638, 4639, 4640, 4642, 4643, 4645, 4647, 4649, 4650, 4652, 4654, 4655, 4656, 4657, 4659, 4660, 4661, 4662, 4663, 4664, 4666, 4668, 4669, 4671, 4672, 4673, 4674, 4675, 4677, 4679, 4681, 4683, 4684, 4685, 4686, 4688, 4691, 4692, 4693, 4694, 4695, 4696, 4697, 4698, 4700, 4702, 4703, 4704, 4705, 4706, 4707, 4709, 4711, 4712, 4713, 4714, 4715, 4716, 4717, 4718, 4719, 4720, 4721, 4722, 4723, 4724, 4725, 4726, 4727, 4728, 4729, 4730, 4731, 4732, 4733, 4734, 4735, 4736, 4739, 4740, 4741, 4742, 4743, 4745, 4747, 4749, 4750, 4751, 4752, 4753, 4754, 4755, 4756, 4757, 4758, 4759, 4760, 4761, 4762, 4763, 4764, 4765, 4767, 4768, 4770, 4771, 4773, 4774, 4775, 4776, 4777, 4778, 4779, 4780, 4781, 4782, 4783, 4784, 4785, 4786, 4787, 4788, 4789, 4790, 4791, 4861, 4930, 5024, 5238, 7100, 7102, 7103, 7104, 7105, 7106, 7107, 7108, 7109, 7110, 7111, 7112, 7113, 7114, 7115, 7116, 7119, 7120, 7121, 7123, 7124, 7125, 7127, 7129, 7130, 7131, 7132, 7133, 7134, 7135, 7136, 7137, 7138, 7139, 7141, 7142, 7143, 7144, 7145, 7146, 7148, 7150, 7151, 7154, 7156, 7157, 7158, 7159, 7161, 7162, 7165, 7170, 7173, 7174, 7178, 7180, 7182, 7184, 7185, 7186, 7189, 7190, 7191, 7192, 7194, 7196, 7197, 7199, 7202, 7204, 7205, 7207, 7212, 7214, 7215, 7216, 7218, 7219, 7220, 7221, 7223, 7227, 7229, 7230, 7231, 7232, 7233, 7234, 7235, 7236, 7237, 7238, 7239, 7240, 7244, 7245, 7248, 7249, 7252, 7254, 7255, 7256, 7258, 7260, 7261, 7263, 7265, 7266, 7267, 7271, 7272, 7273, 7276, 7279, 7281, 7283, 7285, 7286, 7287, 7288, 7289, 7290, 7291, 7292, 7293, 7294, 7295, 7299, 7300, 7302, 7305, 7306, 7307, 7308, 7309, 7311, 7312, 7313, 7315, 7316, 7318, 7322, 7330, 7331, 7334, 7337, 7338, 7340, 7341, 7342, 7344, 7345, 7346, 7347, 7348, 7350, 7351, 7354, 7355, 7356, 7357, 7358, 7362, 7367, 7371, 7372, 7373, 7376, 7379, 7380, 7382, 7385, 7387, 7388, 7390, 7392, 7393, 7394, 7395, 7396, 7397, 7398, 7399, 7400, 7401, 7402, 7403, 7404, 7405, 7406, 7407, 7408, 7409, 7411, 7413, 7416, 7417, 7418, 7419, 7420, 7421, 7422, 7424, 7426, 7427, 7428, 7430, 7433, 7435, 7437, 7439, 7440, 7441, 7442, 7443, 7446, 7448, 7452, 7455, 7456, 7457, 7458, 7459, 7460, 7462, 7464, 7465, 7466, 7469, 7470, 7471, 7472, 7473, 7475, 7479, 7482, 7485, 7486, 7488, 7489, 7490, 7491, 7503, 7505, 7507, 7508, 7510, 7512, 7516, 7517, 7519, 7522, 7524, 7526, 7528, 7530, 7537, 7540, 7542, 7544, 7545, 7549, 7554, 7555, 7556, 7559, 7560, 7561, 7566, 7567, 7568, 7569, 7571, 7572, 7573, 7574, 7575, 7577, 7578, 7579, 7580, 7581, 7582, 7583, 7584, 7586, 7588, 7589, 7591, 7593, 7598, 7600, 7602, 7604, 7605, 7607, 7609, 7612, 7616, 7617, 7621, 7627, 7629, 7630, 7631, 7632, 7634, 7636, 7637, 7640, 7642, 7643, 7645, 7646, 7647, 7648, 7649, 7650, 7651, 7652, 7653, 7655, 7656, 7657, 7658, 7660, 7661, 7662, 7663, 7664, 7665, 7668, 7669, 7670, 7671, 7672, 7673, 7674, 7677, 7678, 7679, 7680, 7681, 7682, 7683, 7684, 8201, 8202, 8203, 8204, 8205, 8206, 8207, 8208, 8209, 8210, 8211, 8212, 8213, 8214, 8216, 8217, 8219, 8220, 8221, 8222, 8223, 8224, 8225, 8226, 8230, 8232, 8233, 8234, 8236, 8237, 8238, 8239, 8240, 8242, 8244, 8245, 8246, 8247, 8248, 8249, 8250, 8251, 8252, 8255, 8256, 8257, 8258, 8261, 8262, 8263, 8264, 8265, 8266, 8267, 8268, 8270, 8271, 8272, 8273, 8274, 8275, 8276, 8277, 8278, 8279, 8280]

# ---------------------------------------------------------------------------
# Newsletter fuer Grundschulen
# ---------------------------------------------------------------------------
container = get_containers_by_path('/unterricht/lernarchiv/newsletter_grundschule/')[0]
base_role = 'no_rights'
role = get_role_by_name(base_role)

# alte Eintraege komplett loeschen
items = DmsUserUrlRole.objects.filter(container=container).filter(role=role)
items.delete()

for org_id in l_grundschulen:
  for user in get_users_with_email_by_org_id(org_id):
    items = DmsUserUrlRole.objects.filter(user=user.user).filter(container=container)
    if len(items) == 0:
      #print user.user.username, org_id
      DmsUserUrlRole.save_user_url_role(DmsUserUrlRole(), user.user.id, container.id, role.id)