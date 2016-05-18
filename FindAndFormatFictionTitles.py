import sublime, sublime_plugin
import re

class FormatFictionCommand(sublime_plugin.TextCommand):
    def run(self, edit, TopTitle = None, topTitlesFormat = None):

        # 替换带章节卷标方法
        def replaceTopTitles(match):
            reStr = self.view.substr(match)
            p = re.compile(r'^第(.{1,5})卷( |)*(.*)第(.{1,10})(章|节)( |)*(.*)')
            replaced = p.sub(r'<h1>第\1卷 <br>\3</h1>\n<h2>第\4\5 <br>\7</h2>', reStr)
            replaced = re.compile(r'( )*</h1>').sub(r'</h1>', replaced)
            print (reStr)
            return replaced

        # 替换不带章节卷标方法
        def replaceTopTitlesWithoutChapter(match):
            reStr = self.view.substr(match)
            p = re.compile(r'^第(.{1,5})卷( |)*(.*)')
            replaced = p.sub(r'<h1>第\1卷 <br>\3</h1>', reStr)
            replaced = re.compile(r'( )*</h1>').sub(r'</h1>', replaced)
            print (reStr)
            return replaced

        # 格式化章节标题——一级
        def formatTitles1():
            matchTitles = self.view.find_all(r'^第(.{1,10})章( |)*(.*)')
            p = re.compile(r'^第(.{1,10})章( |)*(.*)')
            if not matchTitles:
                print ('没有搜索到章节标题')
            else:
                for i in matchTitles[::-1]:
                    reStr = self.view.substr(i)
                    replaced = p.sub(r'<h1>第\1章 <br>\3</h1>', reStr)
                    # replaced = str(replaced).replace("章","节")
                    self.view.replace(edit, i, replaced)
            matchSpecialTitles = self.view.find_all(r'^(楔|楔子)( |)*(.*)')
            if not matchTitles:
                print ('没有搜索到楔子')
            else:
                for i in matchSpecialTitles[::-1]:
                    reStr = self.view.substr(i)
                    replaced = re.compile(r'^(楔|楔子)( |)*(.*)').sub(r'<h1>\1<br>\3</h1>', reStr)
                    # replaced = str(replaced).replace("章","节")
                    self.view.replace(edit, i, replaced)


        # 格式化章节标题——二级
        def formatTitles2():
            matchTitles = self.view.find_all(r'^第(.{1,10})章( |)*(.*)')
            p = re.compile(r'^第(.{1,10})章( |)*(.*)')
            if not matchTitles:
                print ('没有搜索到章节标题')
            else:
                for i in matchTitles[::-1]:
                    reStr = self.view.substr(i)
                    replaced = p.sub(r'<h2>第\1章 <br>\3</h2>', reStr)
                    # replaced = str(replaced).replace("章","节")
                    self.view.replace(edit, i, replaced)

        # 替换空行方法
        def removeBlankLine():
            matchBlankLines = self.view.find_all(r'\n{2,}')
            if not matchBlankLines:
                print ('没有搜索到空行')
            else:
                for i in matchBlankLines[::-1]:
                    self.view.replace(edit, i, '\n')

        # 替换段前空白方法
        def removeWhiteSpacesBeforeParagraph():
            matchWhiteSpaces = self.view.find_all(r'^( )*')
            matchWhiteSpacesCN = self.view.find_all(r'^(　)*')
            if not matchWhiteSpaces:
                print ('没有搜索到段前空白')
            else:
                for i in matchWhiteSpaces[::-1]:
                    self.view.replace(edit, i, '')
                for i in matchWhiteSpacesCN[::-1]:
                    self.view.replace(edit, i, '')

        # 清理不必要的标签
        def removeUselessTab():
            matchUselessTab = self.view.find_all(r'<br></h(\d)>')
            p = re.compile(r'<br></h(\d)>')
            if not matchUselessTab:
                print ('没有搜索到不健康标签')
            else:
                for i in matchUselessTab[::-1]:
                    reStr = self.view.substr(i)
                    replaced = p.sub(r'</h\1>', reStr)
                    self.view.replace(edit, i, replaced)

        topTitlesCN = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十', '二十一', '二十二', '二十三', '二十四', '二十五', '二十六', '二十七', '二十八',]

        topTitlesNum = list(range(1, 31))
        topTitlesNum = [str(i) for i in topTitlesNum]

        # 卷标和章节在同一行时格式化方法
        def replaceTopTitlesWithChapterMutiFormat(topTitlesFormat):
            for i in topTitlesFormat:
                matchTopTitlesWithChapter = self.view.find_all('第' + i + r'卷( |)*(.+)( |)*第(.{1,10})(章|节)(.*)')
                if not matchTopTitlesWithChapter:
                    print ('bad')
                    break
                else:
                    for j in matchTopTitlesWithChapter[:-len(matchTopTitlesWithChapter):-1]:
                        reStr = self.view.substr(j)
                        print (reStr)
                        p = re.compile(r'^(.*)第(.{1,10})(章|节)( |)*(.*)')
                        replaced = p.sub(r'<h2>第\2\3 <br>\5</h2>', reStr)
                        replaced = re.compile(r'( )*</h2>').sub(r'</h2>', replaced)
                        self.view.replace(edit, j, replaced)
                    self.view.replace(edit, matchTopTitlesWithChapter[0], replaceTopTitles(matchTopTitlesWithChapter[0]))

        # 卷标和章节在异行时欲处理
        def preFormat():
            preMatchTopTitles = self.view.find_all('第' + i + r'卷( |)*(.+)( |)*第(.{1,10})(章|节)(.*)')
            p = re.compile(r'^第(.{1,5})卷( |)*(.*)第(.{1,10})(章|节)( |)*(.*)')

        # 卷标和章节在异行时格式化方法
        def replaceTopTitlesWithoutChapterMutiFormat(topTitlesFormat):
            for i in topTitlesFormat:
                matchTopTitlesWithoutChapter = self.view.find_all(r'^第' + i + r'卷( |)*(.{0,15})( |)*$')
                if not matchTopTitlesWithoutChapter:
                    print ('Over')
                    break
                else:
                    for j in matchTopTitlesWithoutChapter[:-len(matchTopTitlesWithoutChapter):-1]:
                        print (self.view.substr(j))
                        self.view.replace(edit, j, '')
                    self.view.replace(edit, matchTopTitlesWithoutChapter[0], replaceTopTitlesWithoutChapter(matchTopTitlesWithoutChapter[0]))
            removeBlankLine()
            removeWhiteSpacesBeforeParagraph()
            formatTitles2()

        # 格式化段落
        def formatParagraph():
            matchParagraphs = self.view.find_all(r'^[^<](.*)')
            p = re.compile(r'^(.*)')
            for i in matchParagraphs[::-1]:
                reStr = self.view.substr(i)
                replaced = p.sub(r'<p>\1</p>', reStr)
                # replaced = str(replaced).replace("章","节")
                self.view.replace(edit, i, replaced)

        if "topTitlesCN" == topTitlesFormat:
            topTitlesFormat = topTitlesCN
        elif "topTitlesNum" == topTitlesFormat:
            topTitlesFormat = topTitlesNum

        removeBlankLine()
        removeWhiteSpacesBeforeParagraph()
        if "withChapter" == TopTitle:
                replaceTopTitlesWithChapterMutiFormat(topTitlesFormat)
        elif "withOutChapter" == TopTitle:
                replaceTopTitlesWithoutChapterMutiFormat(topTitlesFormat)
        elif "NoneTopTitle" == TopTitle:
            formatTitles1()
        formatParagraph()
        removeUselessTab()

        # s = self.view.sel()
        # s = self.view.substr(s)
        #s = re.compile(r'第(.{1,5})章( |)*(.*)').sub(r'<h1>第\1章 <br>\3</h1>',s)
        # whole_region = sublime.Region(0, self.view.size())
        # s = self.view.substr(whole_region)
        # s = self.view.find_all(r'第(.{1,5})章( |)*(.*)' , sublime.IGNORECASE)
        # self.view.replace(edit, whole_region, s)