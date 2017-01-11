%%
%% ampbt.cls: 京都大学工学部情報学科数理工学コース
%%            特別研究報告書用クラスファイル
%%

\NeedsTeXFormat{pLaTeX2e}
\ProvidesClass{ampbt}[2013/05/13 Bachelor thesis class for AMP course]

\newcommand{\amp@ptsize}{11pt}

\newif\if@amp@chapter
\newif\if@amp@duplexing

\newcount\amp@tempcnta
\newdimen\amp@tempdima
\newdimen\amp@spinetitlemaxwidth
\newbox\amp@tempboxa

\DeclareOption{8pt}{\def\amp@ptsize{8pt}}
\DeclareOption{9pt}{\def\amp@ptsize{9pt}}
\DeclareOption{10pt}{\def\amp@ptsize{10pt}}
\DeclareOption{chapter}{\@amp@chaptertrue}
\DeclareOption{duplexing}{\@amp@duplexingtrue}
\DeclareOption*{%
  \PassOptionsToClass{\CurrentOption,\amp@ptsize}{jsbook}%
  \PassOptionsToClass{\CurrentOption,\amp@ptsize}{jsarticle}}
\ProcessOptions\relax

\if@amp@chapter
\LoadClass[report]{jsbook}
\else
\LoadClass{jsarticle}
\fi

\RequirePackage{geometry}
\RequirePackage{graphicx}

\geometry{reset}

\renewcommand{\title}[3]{%
  \def\amp@titlefirst{#1}\def\amp@titlesecond{#2}\def\amp@titlethird{#3}%
  \def\amp@title{#1#2#3}}
\renewcommand{\author}[2]{\def\amp@authorfamily{#1}\def\amp@authorfirst{#2}}
\newcommand{\supervisors}[6]{\def\amp@svfirstname{#1}\def\amp@svfirsttitle{#2}%
  \def\amp@svsecondname{#3}\def\amp@svsecondtitle{#4}%
  \def\amp@svthirdname{#5}\def\amp@svthirdtitle{#6}}
\newcommand{\entrancedate}[2]{\def\amp@entranceyear{#1}\def\amp@entrancemonth{#2}}
\newcommand{\submissiondate}[3]{%
  \def\amp@submissionyear{#1}\def\amp@submissionmonth{#2}\def\amp@submissionday{#3}}
\newcommand{\submissionjay}[1]{\def\amp@submissionjay{#1}}
\long\def\abstract#1{\long\def\amp@abstract{#1}}

\def\abstractname{摘要}
\def\acknowledgmentname{謝辞}

\newcommand\evenclearpage{%
  \clearpage
  \if@amp@duplexing\ifodd\thepage\else
  \thispagestyle{empty}
  \mbox{}
  \clearpage
  \fi\fi}

\newif\ifoutputbody
\outputbodytrue
\newif\ifoutputcover
\outputcovertrue
\newif\ifoutputabstractforsubmission
\outputabstractforsubmissiontrue

\newcommand{\@makecover}{%
  \begin{center}
    \vspace*{12mm}
    \Large{特別研究報告書}\\
    \vspace*{20mm}%

    {\LARGE
      \ifx\amp@titlefirst\@empty　\else\amp@titlefirst\fi\\
      \ifx\amp@titlesecond\@empty　\else\amp@titlesecond\fi\\
      \ifx\amp@titlethird\@empty　\else\amp@titlethird\fi\\}
  \end{center}
  \vspace*{20mm}
  \begin{center}
    {\Large
      \begin{tabular}{rcl}
        指導教員&~~~&\amp@svfirstname　\amp@svfirsttitle\\
        　　　　&~~~&\amp@svsecondname　\amp@svsecondtitle\\
        　　　　&~~~&\amp@svthirdname　\amp@svthirdtitle
      \end{tabular}
    }
  \end{center}
  \vspace*{17mm}
  \begin{center}
    {\Large
      京都大学工学部情報学科\\
      数理工学コース\\
      平成\amp@entranceyear 年\amp@entrancemonth 月入学\\

      \vspace{14mm}%

      {\huge\amp@authorfamily　\amp@authorfirst}\\
      \vspace{14mm}
      平成\amp@submissionyear 年\amp@submissionmonth 月\amp@submissionday 日提出
      \vspace{5mm}
    }
  \end{center}
}

\newcommand{\makecover}{%
  \clearpage
  \newgeometry{hmargin=2truecm,vmargin=3truecm}
  \thispagestyle{empty}
  \begin{center}
    \scalebox{\inv@mag}{
      \begin{tabular}{|p{144mm}|}
        \hline
        \@makecover
        \\
        \hline
    \end{tabular}}
  \end{center}
  \evenclearpage
  \restoregeometry}

\newcommand{\makeinsidecover}{%
  \clearpage
  \newgeometry{hmargin=2truecm,vmargin=3truecm}
  \thispagestyle{empty}
  \begin{center}
    \scalebox{\inv@mag}{
      \begin{tabular}{p{144mm}}
        \@makecover
        \\
    \end{tabular}}
  \end{center}
  \evenclearpage
  \restoregeometry}

\amp@spinetitlemaxwidth=150mm
\newcommand{\@makespine}{%
  %% 題目が長すぎて背表紙のタイトルが2行になったり，氏名の部分まではみ出たりする
  %% ことを防ぐために，タイトルの長さを調べて必要があれば \scalebox で縮小する．
  \let\amp@scalespinetitle\@undefined
  \setbox\amp@tempboxa\hbox{\large\amp@title}%
  \amp@tempdima\wd\amp@tempboxa
  \ifdim\amp@tempdima>\amp@spinetitlemaxwidth
  \edef\amp@tempa{%
    \the\numexpr\number\amp@spinetitlemaxwidth *100/\number\amp@tempdima}%
  \ifnum\amp@tempa=100\else
  \edef\amp@scalespinetitle{.\amp@tempa}% 本当は \amp@tempa<10 の場合の処理が必要
                                        % だが，その場合はそもそも読めないので
                                        % 考慮しない．
  \fi\fi
  \begin{tabular}{|p{7mm}p{150mm}p{70mm}p{33mm}|}
    \hline
    &&&　\\
    &&&　\\
    &\tate\scalebox{\ifx\amp@scalespinetitle\@undefined 1\else\amp@scalespinetitle\fi}{\large\amp@title}
    &\tate\hspace{20mm}{\large\amp@authorfamily　\amp@authorfirst}
    &\tate{\large 平成\,\,\rotatebox[origin=c]{90}{\amp@submissionjay}\,\,年度}\\
    &&&　\\
    &&&　\\
    \hline
\end{tabular}}

\newcommand{\makespine}[1][1]{%
  \clearpage
  \amp@tempcnta=#1\relax
  \newgeometry{hmargin=3truecm,vmargin=.75truecm}
  \thispagestyle{empty}
  \scalebox{\inv@mag}{\tate\parbox{27.67cm}{
      \loop
      \vspace{1.5cm}
      \@makespine
      \advance\amp@tempcnta-1\relax
      \ifnum\amp@tempcnta>0\repeat}}
  \evenclearpage
  \restoregeometry}

\newcommand{\makeabstract}{%
  \clearpage
  \thispagestyle{empty}
  \begin{center}
    \sffamily\bfseries\abstractname
  \end{center}

  \amp@abstract
  \evenclearpage
}

\newcommand{\makeabstractforsubmission}{%
  \clearpage
  \thispagestyle{empty}
  \begin{center}
    {\Large
      \ifx\amp@titlefirst\@empty\else\amp@titlefirst\\\fi
      \ifx\amp@titlesecond\@empty\else\amp@titlesecond\\\fi
      \ifx\amp@titlethird\@empty\else\amp@titlethird\\\fi}

    \vspace{7mm}

    {\Large\amp@authorfamily　\amp@authorfirst}

    \vspace{7mm}

    {\sffamily\bfseries\abstractname}
  \end{center}

  \amp@abstract
  \evenclearpage
}

\newcommand{\maketoc}{%
  \clearpage
  \begingroup
  \pagestyle{empty}
  \tableofcontents
  \evenclearpage
  \endgroup}

\newcommand{\acknowledgment}{%
  \if@amp@chapter
  \addcontentsline{toc}{chapter}{\acknowledgmentname}
  \chapter*{\acknowledgmentname}
  \else
  \section*{\acknowledgmentname}
  \fi}

\endinput
