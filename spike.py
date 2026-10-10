# 1. import fastf1
import fastf1

# 2. ενεργοποίηση cache στον φάκελο "cache"
fastf1.Cache.enable_cache('cache')

# 3. session: 2024, Monza, Race → load

session = fastf1.get_session(2024, 'Monza', 'Race')
session.load()

# 4. print τα results

print(session.results)