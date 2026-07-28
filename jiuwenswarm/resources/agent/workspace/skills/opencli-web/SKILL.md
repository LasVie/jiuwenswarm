---
name: opencli-web
description: Use automatically at the start of any task involving a live website or webpage, including searching, reading, navigation, data extraction, form filling, login, posting, publishing, commenting, or account actions, even when the user does not mention OpenCLI. Route supported site operations through the bundled site router and operation contract before using browser_agent.
---

# OpenCLI Web Router

Use this preinstalled Skill as the automatic entry point for every live website
task. The user does not need to find, install, enable, or select a site Skill.

## Route automatically

1. Read `opencli-web` before starting `browser_agent`.
2. Match both the website and the requested operation against the supported
   websites below.
3. For an exact match, use the Skill tool again with `skill_name` set to
   `opencli-web` and `relative_file_path` set to the listed site module.
4. Follow the site module's declared terminal path. A compact, low-risk public
   read site may make its site `SKILL.md` the terminal contract. Ordinary,
   mixed-risk, private, and mutating sites route to one
   `operations/<operation>.md` terminal contract.
5. When the site is not terminal, use the Skill tool a third time from the
   same main Agent with `skill_name` set to `opencli-web` and
   `relative_file_path` set to the selected operation module's full path.
6. Only after reading the exact terminal contract, call `opencli_execute` with
   exactly its site, logical operation, command, and documented structured
   arguments or payload. The main Agent must make this call immediately after
   its own Skill-tool read so the short-lived disclosure receipt remains
   valid. A documented `disabled` or `quarantined` command has no OpenCLI
   execution authority.
7. Use `browser_agent` only when no exact route exists or the loaded operation
   contract explicitly permits fallback.

Do not search for or install nested site or operation modules as separate
Skills. They are files bundled inside `opencli-web`.

Keep every terminal Skill disclosure in the main agent. Never use `task_tool`,
`sessions_spawn`, a `general-purpose` subagent, `browser_agent`, or a filesystem
tool to read files under the installed `opencli-web` directory. Only the main
Agent's Skill tool is an authorized reader. Optional references are explanatory
only: they cannot carry argument, safety, confirmation, fallback, or execution
authority and they never sign a receipt.

The bundled files in this router are application-managed and refreshed during
JiuwenSwarm startup. Do not customize the installed copy; keep unrelated custom
Skills in their own directories.

## Supported websites

The terminal contract may be the site `SKILL.md` itself for a compact low-risk public-read adapter, or an `operations/*.md` file for ordinary and mixed-risk adapters. Always follow the site router's exact path.

| Website | Commands | Layout | Site module |
|---|---:|---|---|
| 12306 (12306.cn, kyfw.12306.cn) | 9 | `terminal-operation` | `sites/12306/SKILL.md` |
| 1688 (1688.com, www.1688.com) | 7 | `terminal-operation` | `sites/1688/SKILL.md` |
| 1Point3Acres (1point3acres.com, www.1point3acres.com) | 11 | `terminal-operation` | `sites/1point3acres/SKILL.md` |
| 36Kr (www.36kr.com) | 4 | `terminal-operation` | `sites/36kr/SKILL.md` |
| 51Job (jobs.51job.com, we.51job.com) | 4 | `terminal-operation` | `sites/51job/SKILL.md` |
| Aibase (www.aibase.com) | 1 | `terminal-operation` | `sites/aibase/SKILL.md` |
| Amazon (amazon.com) | 9 | `terminal-operation` | `sites/amazon/SKILL.md` |
| Apple Podcasts | 3 | `terminal-site` | `sites/apple-podcasts/SKILL.md` |
| Archive (archive.org) | 4 | `terminal-operation` | `sites/archive/SKILL.md` |
| Arxiv | 4 | `terminal-operation` | `sites/arxiv/SKILL.md` |
| Autohome | 2 | `terminal-site` | `sites/autohome/SKILL.md` |
| Baidu Scholar (xueshu.baidu.com) | 1 | `terminal-operation` | `sites/baidu-scholar/SKILL.md` |
| Band (band.us, www.band.us) | 6 | `terminal-operation` | `sites/band/SKILL.md` |
| Barchart (www.barchart.com) | 4 | `terminal-operation` | `sites/barchart/SKILL.md` |
| Bbc (www.bbc.com) | 2 | `terminal-site` | `sites/bbc/SKILL.md` |
| Bilibili (www.bilibili.com) | 21 | `terminal-operation` | `sites/bilibili/SKILL.md` |
| Binance (data-api.binance.vision) | 11 | `terminal-operation` | `sites/binance/SKILL.md` |
| Bloomberg (feeds.bloomberg.com, www.bloomberg.com) | 13 | `terminal-operation` | `sites/bloomberg/SKILL.md` |
| Bluesky (public.api.bsky.app) | 9 | `terminal-operation` | `sites/bluesky/SKILL.md` |
| Booking (www.booking.com) | 1 | `terminal-operation` | `sites/booking/SKILL.md` |
| Boss (www.zhipin.com, zhipin.com) | 16 | `terminal-operation` | `sites/boss/SKILL.md` |
| Brave (search.brave.com) | 1 | `terminal-operation` | `sites/brave/SKILL.md` |
| Chaoxing (chaoxing.com, mooc2-ans.chaoxing.com) | 4 | `terminal-operation` | `sites/chaoxing/SKILL.md` |
| Chatgpt (chatgpt.com) | 14 | `terminal-operation` | `sites/chatgpt/SKILL.md` |
| Chess (api.chess.com, www.chess.com) | 4 | `terminal-operation` | `sites/chess/SKILL.md` |
| Claude (claude.ai) | 9 | `terminal-operation` | `sites/claude/SKILL.md` |
| Cnki (oversea.cnki.net) | 1 | `terminal-operation` | `sites/cnki/SKILL.md` |
| Coingecko (api.coingecko.com) | 7 | `terminal-operation` | `sites/coingecko/SKILL.md` |
| Confluence (atlassian.net) | 4 | `terminal-operation` | `sites/confluence/SKILL.md` |
| Coupang (coupang.com, www.coupang.com) | 5 | `terminal-operation` | `sites/coupang/SKILL.md` |
| Crates (crates.io) | 2 | `terminal-site` | `sites/crates/SKILL.md` |
| Ctrip (ctrip.com, flights.ctrip.com) | 6 | `terminal-operation` | `sites/ctrip/SKILL.md` |
| Dblp (dblp.org) | 4 | `terminal-operation` | `sites/dblp/SKILL.md` |
| Deepseek (chat.deepseek.com) | 9 | `terminal-operation` | `sites/deepseek/SKILL.md` |
| Defillama (defillama.com) | 2 | `terminal-site` | `sites/defillama/SKILL.md` |
| Devto (dev.to) | 5 | `terminal-operation` | `sites/devto/SKILL.md` |
| Dianping (dianping.com, www.dianping.com) | 4 | `terminal-operation` | `sites/dianping/SKILL.md` |
| Dictionary (api.dictionaryapi.dev) | 3 | `terminal-site` | `sites/dictionary/SKILL.md` |
| Dockerhub (hub.docker.com) | 2 | `terminal-operation` | `sites/dockerhub/SKILL.md` |
| Dongchedi | 6 | `terminal-operation` | `sites/dongchedi/SKILL.md` |
| Douban (book.douban.com, douban.com) | 11 | `terminal-operation` | `sites/douban/SKILL.md` |
| Doubao (www.doubao.com) | 11 | `terminal-operation` | `sites/doubao/SKILL.md` |
| Douyin (creator.douyin.com, www.douyin.com) | 16 | `terminal-operation` | `sites/douyin/SKILL.md` |
| Duckduckgo (duckduckgo.com, html.duckduckgo.com) | 2 | `terminal-operation` | `sites/duckduckgo/SKILL.md` |
| Eastmoney (datacenter-web.eastmoney.com, guba.eastmoney.com) | 14 | `terminal-operation` | `sites/eastmoney/SKILL.md` |
| Endoflife (endoflife.date) | 1 | `terminal-site` | `sites/endoflife/SKILL.md` |
| Facebook (facebook.com, www.facebook.com) | 14 | `terminal-operation` | `sites/facebook/SKILL.md` |
| Flathub (flathub.org) | 2 | `terminal-site` | `sites/flathub/SKILL.md` |
| Flomo (flomoapp.com) | 3 | `terminal-operation` | `sites/flomo/SKILL.md` |
| Gemini (gemini.google.com) | 12 | `terminal-operation` | `sites/gemini/SKILL.md` |
| Geogebra (www.geogebra.org) | 9 | `terminal-operation` | `sites/geogebra/SKILL.md` |
| Gitee (gitee.com) | 5 | `terminal-operation` | `sites/gitee/SKILL.md` |
| Github (github.com) | 2 | `terminal-operation` | `sites/github/SKILL.md` |
| Github Trending (github.com) | 1 | `terminal-site` | `sites/github-trending/SKILL.md` |
| Google (google.com) | 4 | `terminal-operation` | `sites/google/SKILL.md` |
| Google Scholar (scholar.google.com) | 3 | `terminal-operation` | `sites/google-scholar/SKILL.md` |
| Goproxy (proxy.golang.org) | 2 | `terminal-site` | `sites/goproxy/SKILL.md` |
| Gov Law (flk.npc.gov.cn) | 2 | `terminal-operation` | `sites/gov-law/SKILL.md` |
| Gov Policy (sousuo.www.gov.cn, www.gov.cn) | 2 | `terminal-operation` | `sites/gov-policy/SKILL.md` |
| Grok (grok.com) | 15 | `terminal-operation` | `sites/grok/SKILL.md` |
| Guazi | 2 | `terminal-site` | `sites/guazi/SKILL.md` |
| Hackernews (news.ycombinator.com) | 9 | `terminal-operation` | `sites/hackernews/SKILL.md` |
| Hf (huggingface.co) | 7 | `terminal-operation` | `sites/hf/SKILL.md` |
| Hltv (www.hltv.org) | 13 | `terminal-operation` | `sites/hltv/SKILL.md` |
| Homebrew (formulae.brew.sh) | 3 | `terminal-site` | `sites/homebrew/SKILL.md` |
| Huodongxing (www.huodongxing.com) | 1 | `terminal-operation` | `sites/huodongxing/SKILL.md` |
| Hupu (bbs.hupu.com, hupu.com) | 9 | `terminal-operation` | `sites/hupu/SKILL.md` |
| Imdb (www.imdb.com) | 6 | `terminal-operation` | `sites/imdb/SKILL.md` |
| Indeed (www.indeed.com) | 2 | `terminal-operation` | `sites/indeed/SKILL.md` |
| Instagram (instagram.com, www.instagram.com) | 23 | `terminal-operation` | `sites/instagram/SKILL.md` |
| Jd (cart.jd.com, item.jd.com) | 8 | `terminal-operation` | `sites/jd/SKILL.md` |
| Jianyu (jianyu360.cn, www.jianyu360.cn) | 4 | `terminal-operation` | `sites/jianyu/SKILL.md` |
| Jike (m.okjike.com, web.okjike.com) | 12 | `terminal-operation` | `sites/jike/SKILL.md` |
| Jimeng (jimeng.jianying.com) | 6 | `terminal-operation` | `sites/jimeng/SKILL.md` |
| Jira (atlassian.net) | 5 | `terminal-operation` | `sites/jira/SKILL.md` |
| Juejin (api.juejin.cn) | 2 | `terminal-site` | `sites/juejin/SKILL.md` |
| Ke (ke.com) | 6 | `terminal-operation` | `sites/ke/SKILL.md` |
| Kimi (kimi.com) | 29 | `terminal-operation` | `sites/kimi/SKILL.md` |
| Lesswrong (www.lesswrong.com) | 15 | `terminal-operation` | `sites/lesswrong/SKILL.md` |
| Lichess (lichess.org) | 2 | `terminal-site` | `sites/lichess/SKILL.md` |
| Linkedin (www.linkedin.com) | 23 | `terminal-operation` | `sites/linkedin/SKILL.md` |
| Linkedin Learning (linkedin.com, www.linkedin.com) | 5 | `terminal-operation` | `sites/linkedin-learning/SKILL.md` |
| Linux Do (linux.do) | 10 | `terminal-operation` | `sites/linux-do/SKILL.md` |
| Lobsters (lobste.rs) | 6 | `terminal-operation` | `sites/lobsters/SKILL.md` |
| Maimai (maimai.cn) | 3 | `terminal-operation` | `sites/maimai/SKILL.md` |
| Manus (manus.im) | 8 | `terminal-operation` | `sites/manus/SKILL.md` |
| Maven (search.maven.org) | 2 | `terminal-site` | `sites/maven/SKILL.md` |
| Mdn (developer.mozilla.org) | 1 | `terminal-site` | `sites/mdn/SKILL.md` |
| Medium (medium.com) | 4 | `terminal-operation` | `sites/medium/SKILL.md` |
| Mercury (app.mercury.com) | 3 | `terminal-operation` | `sites/mercury/SKILL.md` |
| Mubu (mubu.com) | 5 | `terminal-operation` | `sites/mubu/SKILL.md` |
| Notebooklm (google.com, notebooklm.google.com) | 20 | `terminal-operation` | `sites/notebooklm/SKILL.md` |
| Nowcoder (nowcoder.com, www.nowcoder.com) | 18 | `terminal-operation` | `sites/nowcoder/SKILL.md` |
| Npm (api.npmjs.org, registry.npmjs.org) | 3 | `terminal-site` | `sites/npm/SKILL.md` |
| Nuget (api.nuget.org) | 2 | `terminal-site` | `sites/nuget/SKILL.md` |
| Nvd (services.nvd.nist.gov) | 1 | `terminal-site` | `sites/nvd/SKILL.md` |
| Oeis (oeis.org) | 2 | `terminal-site` | `sites/oeis/SKILL.md` |
| Ones (ones.cn) | 8 | `terminal-operation` | `sites/ones/SKILL.md` |
| Openalex (api.openalex.org) | 2 | `terminal-site` | `sites/openalex/SKILL.md` |
| Openfda (fda.gov) | 2 | `terminal-site` | `sites/openfda/SKILL.md` |
| Openreview (openreview.net) | 5 | `terminal-operation` | `sites/openreview/SKILL.md` |
| Osv (osv.dev) | 2 | `terminal-site` | `sites/osv/SKILL.md` |
| Packagist (packagist.org) | 2 | `terminal-site` | `sites/packagist/SKILL.md` |
| Paperreview (paperreview.ai) | 3 | `terminal-operation` | `sites/paperreview/SKILL.md` |
| Pixiv (pixiv.net, www.pixiv.net) | 8 | `terminal-operation` | `sites/pixiv/SKILL.md` |
| Powerchina (bid.powerchina.cn, powerchina.cn) | 3 | `terminal-operation` | `sites/powerchina/SKILL.md` |
| Producthunt (www.producthunt.com) | 4 | `terminal-operation` | `sites/producthunt/SKILL.md` |
| Pubmed (pubmed.ncbi.nlm.nih.gov) | 9 | `terminal-operation` | `sites/pubmed/SKILL.md` |
| Pypi (pypi.org, pypistats.org) | 2 | `terminal-site` | `sites/pypi/SKILL.md` |
| Quark (pan.quark.cn, quark.cn) | 9 | `terminal-operation` | `sites/quark/SKILL.md` |
| Qwen (qwen.ai, www.qianwen.com) | 10 | `terminal-operation` | `sites/qwen/SKILL.md` |
| Reddit (reddit.com, www.reddit.com) | 21 | `terminal-operation` | `sites/reddit/SKILL.md` |
| Rednote (rednote.com, www.rednote.com) | 9 | `terminal-operation` | `sites/rednote/SKILL.md` |
| Rest Countries (restcountries.com) | 2 | `terminal-site` | `sites/rest-countries/SKILL.md` |
| Reuters (reuters.com, www.reuters.com) | 4 | `terminal-operation` | `sites/reuters/SKILL.md` |
| Rfc (datatracker.ietf.org) | 1 | `terminal-site` | `sites/rfc/SKILL.md` |
| Rubygems (rubygems.org) | 2 | `terminal-site` | `sites/rubygems/SKILL.md` |
| Semanticscholar (api.semanticscholar.org) | 4 | `terminal-operation` | `sites/semanticscholar/SKILL.md` |
| Sinablog (blog.sina.com.cn) | 4 | `terminal-operation` | `sites/sinablog/SKILL.md` |
| Sinafinance (app.cj.sina.com.cn, finance.sina.cn) | 4 | `terminal-operation` | `sites/sinafinance/SKILL.md` |
| Slock (app.slock.ai) | 44 | `terminal-operation` | `sites/slock/SKILL.md` |
| Smzdm (www.smzdm.com) | 1 | `terminal-operation` | `sites/smzdm/SKILL.md` |
| Spotify | 11 | `terminal-operation` | `sites/spotify/SKILL.md` |
| Stackoverflow (stackoverflow.com) | 8 | `terminal-operation` | `sites/stackoverflow/SKILL.md` |
| Steam (store.steampowered.com) | 3 | `terminal-site` | `sites/steam/SKILL.md` |
| Substack (substack.com) | 3 | `terminal-operation` | `sites/substack/SKILL.md` |
| Suno (suno.com) | 6 | `terminal-operation` | `sites/suno/SKILL.md` |
| Taobao (cart.taobao.com, item.taobao.com) | 7 | `terminal-operation` | `sites/taobao/SKILL.md` |
| Tdx (pul.tdx.com.cn) | 1 | `terminal-operation` | `sites/tdx/SKILL.md` |
| Ths (eq.10jqka.com.cn) | 1 | `terminal-operation` | `sites/ths/SKILL.md` |
| Tieba (tieba.baidu.com) | 4 | `terminal-operation` | `sites/tieba/SKILL.md` |
| Tiktok (tiktok.com, www.tiktok.com) | 18 | `terminal-operation` | `sites/tiktok/SKILL.md` |
| Toutiao (mp.toutiao.com, toutiao.com) | 4 | `terminal-operation` | `sites/toutiao/SKILL.md` |
| Tvmaze (tvmaze.com) | 2 | `terminal-site` | `sites/tvmaze/SKILL.md` |
| Twitter (x.com) | 44 | `terminal-operation` | `sites/twitter/SKILL.md` |
| Uisdc (www.uisdc.com) | 1 | `terminal-operation` | `sites/uisdc/SKILL.md` |
| Uiverse (uiverse.io) | 2 | `terminal-operation` | `sites/uiverse/SKILL.md` |
| Upwork (upwork.com, www.upwork.com) | 5 | `terminal-operation` | `sites/upwork/SKILL.md` |
| V2Ex (v2ex.com, www.v2ex.com) | 13 | `terminal-operation` | `sites/v2ex/SKILL.md` |
| Wanfang (s.wanfangdata.com.cn) | 1 | `terminal-operation` | `sites/wanfang/SKILL.md` |
| Wechat Channels (channels.weixin.qq.com) | 3 | `terminal-operation` | `sites/wechat-channels/SKILL.md` |
| Weibo (weibo.com) | 13 | `terminal-operation` | `sites/weibo/SKILL.md` |
| Weixin (mp.weixin.qq.com, weixin.sogou.com) | 4 | `terminal-operation` | `sites/weixin/SKILL.md` |
| Weread (weread.qq.com) | 11 | `terminal-operation` | `sites/weread/SKILL.md` |
| Weread Official (weread.qq.com) | 8 | `terminal-operation` | `sites/weread-official/SKILL.md` |
| Wikidata (www.wikidata.org) | 2 | `terminal-site` | `sites/wikidata/SKILL.md` |
| Wikipedia (wikipedia.org) | 5 | `terminal-operation` | `sites/wikipedia/SKILL.md` |
| Wttr (wttr.in) | 2 | `terminal-site` | `sites/wttr/SKILL.md` |
| Xianyu (goofish.com, www.goofish.com) | 9 | `terminal-operation` | `sites/xianyu/SKILL.md` |
| Xiaoe (h5.xet.citv.cn, study.xiaoe-tech.com) | 7 | `terminal-operation` | `sites/xiaoe/SKILL.md` |
| Xiaohongshu (creator.xiaohongshu.com, www.xiaohongshu.com) | 25 | `terminal-operation` | `sites/xiaohongshu/SKILL.md` |
| Xiaoyuzhou (www.xiaoyuzhoufm.com) | 5 | `terminal-operation` | `sites/xiaoyuzhou/SKILL.md` |
| Xueqiu (danjuanfunds.com, xueqiu.com) | 14 | `terminal-operation` | `sites/xueqiu/SKILL.md` |
| Yahoo (search.yahoo.com) | 1 | `terminal-operation` | `sites/yahoo/SKILL.md` |
| Yahoo Finance (finance.yahoo.com) | 1 | `terminal-operation` | `sites/yahoo-finance/SKILL.md` |
| Yollomi (yollomi.com) | 12 | `terminal-operation` | `sites/yollomi/SKILL.md` |
| Youdao (share.note.youdao.com) | 1 | `terminal-operation` | `sites/youdao/SKILL.md` |
| Youtube (www.youtube.com) | 16 | `terminal-operation` | `sites/youtube/SKILL.md` |
| Yuanbao (yuanbao.tencent.com) | 9 | `terminal-operation` | `sites/yuanbao/SKILL.md` |
| Zhihu (www.zhihu.com, zhihu.com) | 22 | `terminal-operation` | `sites/zhihu/SKILL.md` |
| Zlibrary (z-library.im) | 2 | `terminal-operation` | `sites/zlibrary/SKILL.md` |
| Zsxq (wx.zsxq.com, zsxq.com) | 7 | `terminal-operation` | `sites/zsxq/SKILL.md` |

## Execute documented commands

- `opencli_execute` is the only authorized entry for OpenCLI operations. Never invoke its
  underlying package executor, Python compatibility wrapper, adapter command,
  runtime probe, or executable through BashTool, PowerShell, execute-code, a
  subagent, or a filesystem tool.
- Preserve structured argument types and absolute Windows payload paths
  exactly as documented by the terminal contract. The tool constructs a
  reviewed shell-free argv and rejects executable, prefix-argument,
  environment, site, command, and unknown-argument overrides.
- On Windows, use `shell_type: "auto"` for any separately documented,
  non-OpenCLI fallback subprocess. Do not force `bash` or `sh` merely to run
  Python or translate Windows paths.
- Do not invoke `scripts/opencli_runtime.py` separately. A structured or
  documented guarded executor runs the shared readiness check internally
  before adapter dispatch and classifies typed connection failures itself.

## Enforce one automation path

- Never run OpenCLI and `browser_agent` concurrently for the same operation.
- A route exists only when the root router lists the site, the site router
  lists the capability group, and the runtime manifest binds the selected
  terminal contract to the exact command. Do not infer write support from a
  read command.
- Invoke only the structured entry documented by the loaded terminal
  contract. Catalog discovery and help output never authorize an undocumented,
  disabled, or quarantined command.
- Preserve all channel-specific confirmation gates. An operation module cannot
  waive a required user approval or A2UI confirmation.
- If a write process starts, do not repeat the operation through
  `browser_agent`, even after a timeout or ambiguous result. Prefer a supported
  read-only verification; otherwise stop and report uncertainty.
- A missing executable, disabled or unreadable module, unsupported operation,
  or other provable pre-execution infrastructure failure is fallback-safe.
- Read-only OpenCLI failures may fall back to `browser_agent` when that does not
  risk duplicating a side effect.

Use `opencli list -f json` only to inspect locally installed adapter
capabilities. Add reviewed site and operation modules before routing production
work to a new adapter.
