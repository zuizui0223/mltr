# Paper A 指導教員レビュー用 brief

## まず伝えたい結論

Paper A は、当初の「新しい coarsest source-relative repair 定理」を主張する theorem-first 論文から、**構造変化後に既存の生態学的状態分類を管理判断へ再利用してよいかを監査し、失敗を exact monitoring repair の要件へ変換する理論**へ全面的に組み替えた。

現在の中心問いは：

> ある生態系管理で既に使われている状態分類は、種の入れ替わり・相互作用の再配線・生息地変化・新しい介入の導入後にも、管理判断に必要な情報を十分保持しているか。保持していないなら、現在のモニタリング変数で必要な区別を回復できるか。できるなら最小費用で何を測るべきか。できないなら、どの状態対が現在の観測系では区別不能なのか。

## 先行研究精査で撤回した新規性

以下は既知として本文・補足で明示的に位置づけ直した。

- 任意の初期分割からの coarsest stable refinement：Paige & Tarjan (1987)
- MDP の coarsest homogeneous refinement：Givan, Dean & Greig (2003)
- MDP state abstraction の体系化：Li, Walsh & Littman (2006)
- source MDP から target MDP への state abstraction transfer：Walsh, Li & Littman (2006)
- 異なる decision process 間の homomorphism：Ravindran & Barto (2003)
- state-and-transition model を用いた targeted monitoring：Jones et al. (2023)
- 生態学的 value of information：Canessa et al. (2015)
- history-preserving / path-sensitive formalism：既存分野として認識
- state identification / sensor-selection / set-cover 型の観測選択：一般的な形式・制御分野に既存

したがって、**generic refinement、generic abstraction transfer、targeted monitoring、VoI、history-sensitive equivalence、set-cover 自体を新規とは主張しない**。

## 現在の主結果

### 1. Decision-sufficiency audit

inherited state 内で target の output、実施可能 action、action 後の successor state が一様かを検査する。一様なら旧分類をそのまま管理へ使える。

### 2. Local obstruction

旧分類が失敗するとき、「同じ旧stateなのにtarget actionへの応答が異なる」具体的な状態対を返す。standard refinement は、そのtarget interfaceで必要な least exact distinction を定める supporting machinery として使う。

### 3. Exact monitoring realization — 現在の applied centerpiece

candidate measurement `z_j` の集合 `S` が repaired state `Q*` を実現するとは、

`Q*(x)=d_S(C(x),z_S(x))`

を満たす decoder が存在することと定義した。

これは、

`E={(x,x'): C(x)=C(x'), Q*(x)!=Q*(x')}`

の全 obstruction pair を、選択測定の少なくとも1つが分離することと必要十分。

この結果から3通りの実務出力が得られる。

1. inherited state が pass → 構造的monitoring redesignは不要。
2. stateはfailするがcandidate libraryが全pairをcover → exact recovery可能。測定費用を与えれば minimum-cost exact subset を求められる。
3. candidate library全体でもcoverできないpairがある → **現在のmonitoring libraryではdecision-sufficient stateを回復不能**。未被覆pairが明示的なimpossibility certificateになる。

つまり「もっとデータを取る」ではなく、**何を区別できなければいけないか／今の観測系でそれが可能か**を先に決める。

## replayで追加した monitoring witness

local witness は

- inherited labels `(0,0,1)`
- repaired labels `(0,1,2)`
- obstruction pair `(0,1)`

候補測定のillustrative libraryでは：

- `substitute_response_capacity` は `(0,1)` を分離
- abundance proxy と soil-condition proxy は分離しない

したがって：

- full library：exact recovery feasible
- minimum exact subset：`substitute_response_capacity`
- illustrative acquisition cost：`1.0`
- abundance + soil-condition だけのsublibrary：infeasible
- uncovered pair `(0,1)` がそのcertificate

これらのmeasurement value/costは実証値ではなく、monitoring theoremを再現する有限witness。

## 植物–送粉者例で何が起きるか

旧分類では Site A と B が同じ pollination state にまとめられている。

pollinator turnover 後、新しい介入が substitute-pollinator response の違いを露出すると、A と B を同じ管理stateとして扱えなくなる。local obstruction は A--B pair であり、修復後に区別すべき生態学的差は substitute-response capacity になる。

illustrative decision layer として：

- benefit `B=1`
- `c_A=0.20`, `c_B=0.35`
- `p_A=0.25`, `p_B=0.80`

を置くと、旧 pooled state は安い A を選ぶが、repair 後は B を選ぶ。旧判断の one-step regret は `0.40`。一般的な逆転条件は

`p_B - p_A > (c_B - c_A)/B`

であり、実証推定値ではなく sensitivity example と明記している。

## supporting results

- **Minimum conditional label information**：任意のexact refinement `P` に対し `H(Q*|C) <= H(P|C)` を証明済み。
- **No universal defect-regret ordering**：任意の `d>=1` と `r>=0` に対し defect=`d`, regret=`r` の有限exact-repair問題を構成できることを証明済み。
- **Source-relative exact repair**：有限settingについて停止・fixed-point exactness・unique coarsenessを自己完結証明済み。先行研究はprior-art statusの引用。
- **Route context**：alternative routes が同じterminal carried mapならhistory不要、異なる場合のみdistinct contextが必要。secondary closure resultとして扱う。

## 論文の構造的リスク

proof gap は閉じた。一方、**generic な数学的新規性を主張しない以上、採否は生態学的問題設定の一般性と重要性に強く依存する**という評価は変わらない。

ただし現在は framing だけではない。Paper A は、audit failure を

- pass/fail
- obstruction pair
- candidate monitoring library の exact feasibility / impossibility
- uncovered-pair certificate
- minimum-cost exact measurement selection
- downstream management consequence

へ変換する。

Jones et al. (2023) は predefined state を区別する観測変数・thresholdを選ぶ。本稿はその一段上流で、**predefined state 自体が新しい介入に対してまだ妥当かを検査し、失効したときに初めて「区別すべきpair」を生成する**。Canessa et al. (2015) の VoI はさらに下流で、その情報を取得する価値を評価する。

したがって現在の主線は：

`inherited management state -> structural audit -> obstruction -> monitoring feasibility/impossibility -> minimum monitoring cost -> decision consequence`

## 現在の推奨

Theoretical Ecology を第一候補のままにする。本文では Monitoring realization を applied centerpiece に固定し、`coarsest refinement`、`transport defect`、historyをheadlineへ戻さない。

教員に本当に判断してほしいのは次の2点だけ：

1. **この「既存の管理stateが構造変化後もdecision-sufficientかを監査し、失敗をexact monitoring requirementへ変換する」という問いは、Theoretical Ecology で独立論文として十分一般的・重要か。**
2. **理論＋illustrative decision example で投稿し、実データによる検証を別稿にするか。それとも実証1例を今稿に必須と考えるか。**

もし Theoretical Ecology が formal-methods 寄りすぎると判断する場合、Ecological Modelling を即時fallbackとする。
