from news_bridge.models import Source

ENGLISH_SOURCES = [
    Source(
        name="CNN World",
        language="en",
        feed_url="https://rss.cnn.com/rss/edition_world.rss",
    ),
    Source(
        name="BBC World",
        language="en",
        feed_url="https://feeds.bbci.co.uk/news/world/rss.xml",
    ),
]

CHINESE_SOURCES = [
    Source(
        name="BBC 中文",
        language="zh",
        feed_url="https://feeds.bbci.co.uk/zhongwen/simp/rss.xml",
    ),
    Source(
        name="新华网 国内",
        language="zh",
        feed_url="http://www.news.cn/fortunepro/rss/zgjj.xml",
    ),
]
