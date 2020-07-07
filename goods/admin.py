from django.contrib import admin
from django.core.cache import cache
from goods import task
from goods.models import GoodsType, IndexPromotionBanner, IndexGoodsBanner, IndexTypeGoodBanner, GoodsSKU, Goods


# Register your models here.
# 抽象出管理类
class BaseModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        '''新增或更新表中的数据时调用'''
        super().save_model(request, obj, form, change)

        # 发出任务，让celery worker重新生成首页静态页
        task.generate_static_index_html.delay()

        # 当首页有更新时,要对缓存数据进行清除
        cache.delete(':1:index_page_data')

    def delete_model(self, request, obj):
        '''删除表中的数据时调用'''
        super().delete_model(request, obj)
        # 发出任务，让celery worker重新生成首页静态页
        task.generate_static_index_html.delay()



class GoodsTypeAdmin(BaseModelAdmin):
    pass


class IndexGoodsBannerAdmin(BaseModelAdmin):
    pass


class IndexTypeGoodsBannerAdmin(BaseModelAdmin):
    pass


class IndexPromotionBannerAdmin(BaseModelAdmin):
    pass

class IndexGoodsSKUAdmin(BaseModelAdmin):
    pass

class IndexGoodsAdmin(BaseModelAdmin):
    pass

# 注册
admin.site.register(GoodsType, GoodsTypeAdmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(IndexTypeGoodBanner, IndexTypeGoodsBannerAdmin)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)
admin.site.register(GoodsSKU, IndexGoodsSKUAdmin)
admin.site.register(Goods, IndexGoodsAdmin)

