package main
 
import (
        "fmt"
        "io"
        "net/http"
        "os"
        "regexp"
        "strconv"
        "strings"
)
var count int
func main() {
        var start, end int
        fmt.Print("起始页(>=1):")
        fmt.Scan(&start)
        fmt.Print("终止页(>=起始页[适度爬取,太多小心IP被封哦]):")
        fmt.Scan(&end)
 
        //创建文件
        fc,err:=os.Create("BookList.txt")
        if err!=nil{
                fmt.Println("os.Create err",err)
                return
        }
        fc.Close()
 
        //循环读取每一页
        for i := start; i <= end; i++ {
                working(i)
        }
        fmt.Println("爬取完毕,马上闪开!!!")
}
func working(idx int) {
 
        //打开文件
        fo,err:=os.OpenFile("BookList.txt",os.O_APPEND,6)
        if err!=nil{
                fmt.Println("os.OpenFile err",err)
                return
        }
        defer fo.Close()
 
        url := "https://www.bukebook.cn/page/" + strconv.Itoa(idx)
        result, err := httpGet(url, idx)
        if err != nil {
                fmt.Println("检查网络,或者IP被封了...")
                return
        }
 
        //正则处理信息获得bookID
        //正则规则
        bookIDRule :=`class="greatwp-fp04-post-title"><a href="https://www.bukebook.cn/([0-9]+).html" rel="bookmark">`
        bookNameRule := `.html">《(?s:(.*?))</a></h2>`
        CTUrlRule := `<a class="ordown-button" href="(?s:(.*?))" target="_blank">城通网盘</a>`
        psdRule := `<strong>提取秘钥： </strong>(?s:(.*?))   </br>`
 
        allID:=regexpData(result, bookIDRule)
        for i,tmpID:=range allID{
                bookID:=tmpID[1]
                //拼接下载页URL
                dlUrl:="https://www.bukebook.cn/wp-content/plugins/ordown/down.php?id="+bookID
                //访问下载页
                dlResult,err:=httpGet(dlUrl,i)
                if err!=nil{
                        fmt.Println("dl httpGet err",err)
                        return
                }
                //处理数据获取书名,下载地址及密码
                allBookName:=regexpData(dlResult,bookNameRule)
                allCTUrl:=regexpData(dlResult,CTUrlRule)
                allPsd:=regexpData(dlResult,psdRule)
                //fmt.Println(dlResult)
                for _,tmpBookName:=range allBookName{
                        bookName:=tmpBookName[1]
                        //判断网盘类型
                        if strings.Contains(dlResult,"百度云盘"){
                                count++
                                //封装百度网盘URL
                                BDUrl:="https://www.bukebook.cn/wp-content/plugins/ordown/download1.php?id="+bookID
                                //获取网盘密码
                                for _,tmpPsd:=range allPsd{
                                        //存储书名及城通地址
                                        fo.Write([]byte(strconv.Itoa(count)+".《"+bookName+"\n"+BDUrl+"  "+tmpPsd[1]+"\n"))
                                        fmt.Println("《"+bookName+" 完成\n")
                                }
                        }else{
                                count++
                                //获取城通网址
                                for _,tmpCTUrl:=range allCTUrl{
                                        //存储书名及城通地址
                                        fo.Write([]byte(strconv.Itoa(count)+".《"+bookName+"\n"+tmpCTUrl[1]+"\n"))
                                        fmt.Println("《"+bookName+" 完成\n")
                                }
 
                        }
                }
 
        }
 
}
func regexpData(data, rule string) [][]string {
        reg := regexp.MustCompile(rule)
        return reg.FindAllStringSubmatch(data, -1)
}
func httpGet(url string, idx int) (result string, err error) {
        resp, err1 := http.Get(url)
        if err1 != nil {
                err = err1
                return
        }
        defer resp.Body.Close()
        buf := make([]byte, 4096)
        for {
                n, err2 := resp.Body.Read(buf)
                if n == 0 {
                        break
                }
                if err2 != nil && err2 != io.EOF {
                        err = err2
                        return
                }
                result += string(buf[:n])
        }
        return
}