from rest_framework import filters

# Custom generic filtering

# Some issues occur when applied, default backends get applied
class FollowersCountFilterBackend(filters.BaseFilterBackend):
    """
   	Filter that applies ordering according to the followers_count
    """
    def filter_queryset(self, request, queryset, view):
        
        queryset = sorted(queryset, key=lambda x: x.followers_count(), reverse=True)

        return queryset



