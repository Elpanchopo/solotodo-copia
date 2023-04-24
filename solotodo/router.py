from rest_framework import routers

from solotodo.views import UserViewSet, StoreViewSet, LanguageViewSet, \
    CurrencyViewSet, CountryViewSet, StoreTypeViewSet, CategoryViewSet, \
    StoreUpdateLogViewSet, EntityViewSet, ProductViewSet, \
    NumberFormatViewSet, WebsiteViewSet, \
    LeadViewSet, EntityHistoryViewSet, VisitViewSet, ResourceViewSet, \
    RatingViewSet, ProductPictureViewSet, FilesViewSet, BrandViewSet, \
    EntitySectionPositionViewSet, StoreSectionViewSet, ProductVideoViewSet, \
    BundleViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'websites', WebsiteViewSet)
router.register(r'stores', StoreViewSet)
router.register(r'number_formats', NumberFormatViewSet)
router.register(r'languages', LanguageViewSet)
router.register(r'store_types', StoreTypeViewSet)
router.register(r'currencies', CurrencyViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'bundles', BundleViewSet)
router.register(r'store_update_logs', StoreUpdateLogViewSet)
router.register(r'entities', EntityViewSet)
router.register(r'entity_histories', EntityHistoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'leads', LeadViewSet)
router.register(r'visits', VisitViewSet)
router.register(r'ratings', RatingViewSet)
router.register(r'resources', ResourceViewSet, basename='resources')
router.register(r'product_pictures', ProductPictureViewSet)
router.register(r'files', FilesViewSet, basename='files')
router.register(r'brands', BrandViewSet)
router.register(r'entity_section_positions', EntitySectionPositionViewSet)
router.register(r'store_sections', StoreSectionViewSet)
router.register(r'product_videos', ProductVideoViewSet)
