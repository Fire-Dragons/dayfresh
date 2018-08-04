from django.contrib import admin
from goods.models import *
from django.core.cache import cache


def delete_model(modeladmin,request,queryset):
    print('delete')
    for obj in queryset:
        # obj.is_delete = True
        obj.delete()



class BaseAdmin(admin.ModelAdmin):
    #清楚缓存
    cache.delete('cache_index_page_data')
    #调用自写的删除功能
    actions = [delete_model]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)



class GoodsTypeAdmin(BaseAdmin):
    pass

class GoodsSKUAdmin(BaseAdmin):
    pass

class GoodsAdmin(BaseAdmin):
    pass

class GoodsImageAdmin(BaseAdmin):
    pass

class IndexGoodsBannerAdmin(BaseAdmin):
    pass

class IndexTypeGoodsBannerAdmin(BaseAdmin):
    pass

class IndexPromotionBannerAdmin(BaseAdmin):
    pass

admin.site.register(GoodsType,GoodsTypeAdmin)
admin.site.register(GoodsSKU,GoodsSKUAdmin)
admin.site.register(Goods,GoodsAdmin)
admin.site.register(GoodsImage,GoodsImageAdmin)
admin.site.register(IndexGoodsBanner,IndexGoodsBannerAdmin)
admin.site.register(IndexTypeGoodsBanner,IndexTypeGoodsBannerAdmin)
admin.site.register(IndexPromotionBanner,IndexPromotionBannerAdmin)