Name:           antlrworks
Version:        1.4
Release:        7
Summary:        Grammar development environment for ANTLR v3 grammars

Group:          Development/Java
License:        BSD
URL:            https://www.antlr.org/works
Source0:        http://www.antlr.org/download/%{name}-%{version}-src.zip
Source1:        antlrworks.sh
Source2:        antlrworks.desktop
# Disable embedding of dependency jars file into antlrworks jar file
Patch0:         antlrworks-1.4-build.patch
# Add xdg-open and epiphany as available web browsers to open help (sent
# upstream)
Patch1:         antlrworks-1.4-browsers.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ant
BuildRequires:  antlr3-tool
BuildRequires:  desktop-file-utils
BuildRequires:  jgoodies-forms
Requires:       antlr3-tool
Requires:       graphviz
# Owns /usr/share/icons/hicolor
Requires:       hicolor-icon-theme
Requires:       java-devel >= 0:1.6.0
Requires:       jgoodies-forms
BuildArch:      noarch


%description
ANTLRWorks is a novel grammar development environment for ANTLR v3 grammars
written by Jean Bovet (with suggested use cases from Terence Parr). It combines
an excellent grammar-aware editor with an interpreter for rapid prototyping and
a language-agnostic debugger for isolating grammar errors. ANTLRWorks helps
eliminate grammar nondeterminisms, one of the most difficult problems for
beginners and experts alike, by highlighting nondeterministic paths in the
syntax diagram associated with a grammar. ANTLRWorks' goal is to make grammars
more accessible to the average programmer, improve maintainability and
readability of grammars by providing excellent grammar navigation and
refactoring tools, and address the most common questions and problems
encountered by grammar developers.


%prep
%setup -q -c
%patch0 -p0 -b .build
%patch1 -p1 -b .browsers

find -name '*.class' -o -name '*.jar' -exec rm '{}' \;


%build
export CLASSPATH=$(build-classpath antlr antlr3 antlr3-runtime jgoodies-forms stringtemplate)
ant build


%install
rm -rf $RPM_BUILD_ROOT
install -Dpm 0644 dist/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

install -Dpm 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/%{name}

desktop-file-install \
  --dir=$RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE2}

install -Dpm 0644 resources/icons/app.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
for i in 16 32 64; do
  install -Dpm 0644 resources/icons/app_${i}x$i.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x$i/apps/%{name}.png
done

desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop


%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_javadir}/*.jar


